from flask import Flask, request
import json
import sys
import subprocess
import requests
from github_token import github_token

app = Flask(__name__)

# Runs on every subscribed event
@app.route("/", methods=["POST"])
def handle():
	run_build()
	static_analysis(request.data)
	run_tests(request.data)


# Run build script
def run_build():
	res = subprocess.run(["bash", "build.sh"])
	if res.returncode == 0:
		return True
	else:
		return False


# The CI server performs static analysis on the updated branch
def static_analysis(req):
	pass


# The CI server executes the test suite on the branch that was changed
def run_tests(req):
	pass


# The CI server sets commit status
def notify(req, status):
	try:
		full_name = req["repository"]["full_name"]
		SHA = req["after"]

		headers = {
			'Accept': 'application/vnd.github+json',
			'Authorization': f'Bearer {github_token}',
			'X-GitHub-Api-Version': '2022-11-28',
			'Content-Type': 'application/x-www-form-urlencoded',
		}
		data = '{"state":"' + status + '"}'

		response = requests.post(f'https://api.github.com/repos/{full_name}/statuses/{SHA}', headers=headers, data=data)
		
		response_json = response.json()
		response.raise_for_status()

		if response.status_code == 201:
			return response_json
	
	except requests.exceptions.RequestException as e:
		print(e)
		raise
	


