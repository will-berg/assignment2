from flask import Flask, request
import json
import sys
import subprocess

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
	pass

