"""
The auto updater service that makes sure the running instance use the current version available on the main branch.
Whenever it receives a push event from the webhook, it will fetch the latests code, built it and then hot reload the services without downtime.
"""
from flask import Flask, request
import os
import json

app = Flask(__name__)

# Handles the webhook requests from GitHub.
# When it receives a push event, it will update and restart the services.
@app.route("/", methods=["POST"])
def update():
	if not request.headers.get('User-Agent').startswith('GitHub-Hookshot'):
		return ({'message': 'Only GitHub can call this endpoint.'}, 403)

	event = request.headers.get('X-GitHub-Event')

	if event is None:
		return ({'message': 'The event type wasn\'t specified.'}, 400)

	data = json.loads(request.data)

	if event == 'push':
		if data['ref'] == 'refs/heads/main':
			if app.testing == False:
				update_and_restart()
			return ({'message': 'Update process started.'}, 200)
		else:
			return ({'message': 'Push not on main, skipping update.'}, 200)
	elif event == 'ping':
		return ({}, 200)
	else:
		return ({'message': f'Event {event} is not supported.'}, 400)

# Invokes a utility script that will fetch the latest code from main and
# hot reload the services.
# The script runs in a separate process to ensure it will not reload itself.
def update_and_restart():
	pid = os.fork()

	if pid == 0:
		os.execl('./util/update_restart.sh', './util/update_restart.sh')

	return

