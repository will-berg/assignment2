"""
The CI server runs the CI pipeline when a subscribed event occurs at the GitHub repository.
This includes running the build, performing static analysis, testing the code, and then
notifying GitHub of the results.
"""
from flask import Flask, request
import os
import json
import subprocess
import requests
from github_token import github_token
from datetime import date

app = Flask(__name__)

# Handles POST requests to the root endpoint. On push events, the repo is cloned and
# entered and the pipeline is executed.
@app.route("/", methods=["POST"])
def handle():
	if not request.headers.get('User-Agent').startswith('GitHub-Hookshot'):
		return ({'message': 'Only GitHub can call this endpoint.'}, 403)

	event = request.headers.get('X-GitHub-Event')

	if event == 'ping':
		return ({'message': 'We are here \o/'}, 200)
	elif event == 'push':
		pid = os.fork()
		if pid == 0:
			req = json.loads(request.data)

			old = os.getcwd()
			dir_name = f"/tmp/{req['after']}"
			if not os.path.exists(dir_name):
				os.mkdir(dir_name)
			subprocess.call(["bash", "util/git_setup.sh", f"{req['repository']['clone_url']}", f"{req['after']}"])
			os.chdir(dir_name)
			run_pipeline(req)

			os.chdir(old)
			os._exit(0)
		return {'message': 'webhook done'}

# Runs the build, performs linting on the code, and runs the relevant tests.
# Notifies GitHub along every step of the way and stores outputs in a file.
def run_pipeline(req):
	notify(req, 'pending')
	file_name = f'/srv/ci/{req["after"]}'
	todays_date = str(date.today())
	with open(file_name, "ab") as file:
		file.write(bytes("Commit id: " + req["after"] + " Build date: " + todays_date + "\n", 'utf-8'))
		res, output = run_build()
		file.write(output)
		file.write(bytes("\n",'utf-8'))
		if res == False:
			notify(req, 'error')
			return
		res, output = static_analysis()
		file.write(output)
		file.write(bytes("\n",'utf-8'))
		if res == False:
			notify(req, 'error')
			return
		res, output = run_tests()
		file.write(output)
		file.write(bytes("\n",'utf-8'))
		if res == False:
			notify(req, 'error')
			return
		notify(req, 'success')


# Runs the build script (activates virtual environment, installs dependencies).
# Returns boolean indicating a pass or fail along with the build output.
def run_build():
	res = subprocess.run(["bash", "build.sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if res.returncode == 0:
		return True, res.stdout
	else:
		return False, res.stdout


# Runs the lint script (static analysis on ci_server.py, web.py, and updater.py).
# Returns boolean indicating a pass or fail along with the pylint output.
def static_analysis():
	res = subprocess.run(["bash", "lint.sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if res.returncode == 0:
		return True, res.stdout
	else:
		return False, res.stdout


# Runs the test script (unit testing ci_server.py and updater.py).
# Returns boolean indicating a pass or fail along with the testing output.
def run_tests():
	res = subprocess.run(["bash", "test.sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if res.returncode == 0:
		return True, res.stdout
	else:
		return False, res.stdout


# Notifies github with POST request that sets commit status. Also includes a target URL
# that contains the relevant outputs generated during the pipeline process.
def notify(req, status):
	try:

		headers = {
			'Accept': 'application/vnd.github+json',
			'Authorization': f'Bearer {github_token}',
			'X-GitHub-Api-Version': '2022-11-28',
			'Content-Type': 'application/json',
		}
		data = {"state": status, "context": "ci_server", "description": "This is a test description", "target_url": f'http://molly.aronbergman.se/{req["after"]}'}

		response = requests.post(f'https://api.github.com/repos/{req["repository"]["full_name"]}/statuses/{req["after"]}', headers=headers, data=json.dumps(data))

		response_json = response.json()
		response.raise_for_status()

		if response.status_code == 201:
			return response_json

	except requests.exceptions.RequestException as e:
		print(e)
		raise
