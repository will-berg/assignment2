from flask import Flask, request
import os
import json
import sys
import subprocess
import requests
from github_token import github_token

app = Flask(__name__)

# Runs on every subscribed event
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

def run_pipeline(req):
	file_name = f'/srv/ci/{req["after"]}'
	with open(file_name, "ab") as file:
		res, output = run_build()
		file.write(output)
		if res == False:
			notify(req, 'error')
			return
		res, output = static_analysis()
		file.write(output)
		if res == False:
			notify(req, 'error')
			return
		res, output = run_tests()
		file.write(output)
		if res == False:
			notify(req, 'error')
			return
		notify(req, 'success')


# Run build script
def run_build():
	res = subprocess.run(["bash", "build.sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if res.returncode == 0:
		return True, res.stdout
	else:
		return False, res.stdout


# The CI server performs static analysis on the updated branch
def static_analysis():
	res = subprocess.run(["bash", "lint.sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if res.returncode == 0:
		return True, res.stdout
	else:
		return False, res.stdout


# The CI server executes the test suite on the branch that was changed
def run_tests():
	res = subprocess.run(["bash", "test.sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if res.returncode == 0:
		return True, res.stdout
	else:
		return False, res.stdout


# The CI server sets commit status
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
