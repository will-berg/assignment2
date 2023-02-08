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
		req = json.loads(request.data)

		old = os.getcwd()
		dir_name = f"/tmp/{req['after']}"
		if not os.path.exists(dir_name):
			os.mkdir(dir_name)
		os.chdir(dir_name)
		subprocess.call(["bash", "util/git_setup.sh", f"{req['repository']['clone_url']}", f"{req['after']}"])

		run_pipeline(req)

		os.chdir(old)
		return {'message': 'webhook done'}

def run_pipeline(req):
	res = run_build()
	if res == False:
		notify(req, 'error')
		return
	res = static_analysis()
	if res == False:
		notify(req, 'error')
		return
	res = run_tests()
	if res == False:
		notify(req, 'error')
		return
	notify(req, 'success')

# Run build script
def run_build():
	res = subprocess.run(["bash", "build.sh"])
	if res.returncode == 0:
		return True
	else:
		return False


# The CI server performs static analysis on the updated branch
def static_analysis():
	res = subprocess.run(["bash", "lint.sh"], stdout=subprocess.PIPE)
	pylint_output = res.stdout
	if res.returncode == 0:
		return True
	else:
		return False


# The CI server executes the test suite on the branch that was changed
def run_tests():
	res = subprocess.run(["bash", "test.sh"], stdout=subprocess.PIPE)
	pylint_output = res.stdout
	if res.returncode == 0:
		return True
	else:
		return False


# The CI server sets commit status
# req: The input request (json)
# name: The name of the check. For example, "code-coverage". (string)
# conclusion: The final conclusion of the check. Can be one of: action_required, cancelled, failure, neutral, success, skipped, stale, timed_out. (string)
# title: The title of the check run. (string)
# summary: The summary of the check run. This parameter supports Markdown. Maximum length: 65535 characters. (string)
# text: The details of the check run. This parameter supports Markdown. Maximum length: 65535 characters. (string)
def notify(req, name, conclusion, title, summary, text):
	try:
		headers = {
			'Accept': 'application/vnd.github+json',
			'Authorization': f'Bearer {github_token}',
			'X-GitHub-Api-Version': '2022-11-28',
			'Content-Type': 'application/json',
		}
		output = {"title": title, "summary": summary, "text": text}
		repo_full_name = req["repository"]["full_name"]
		data = {"name": name, "head_sha": req["after"], "conclusion": conclusion, "output": output}

		response = requests.post(f'https://api.github.com/repos/{repo_full_name}/check-runs', headers=headers, data=data)
		
		response_json = response.json()
		response.raise_for_status()

		if response.status_code == 201:
			return response_json

	except requests.exceptions.RequestException as e:
		print(e)
		raise
