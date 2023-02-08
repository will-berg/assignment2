from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def update():
	if not request.headers.get('User-Agent').startswith('GitHub-Hookshot'):
		return ({'message': 'Only GitHub can call this endpoint.'}, 403)

	event = request.headers.get('X-GitHub-Event')

	if event is None:
		return ({'message': 'The event type wasn\'t specified.'}, 400)

	if event == 'push': 
		if app.testing == False:
			update_and_restart()
			return ({'message': 'Update process started.'}, 200)
	elif event == 'ping':
		return ({}, 200)
	else:
		return ({'message': f'Event {event} is not supported.'}, 400)

def update_and_restart():
	pid = os.fork()

	if pid == 0:
		os.execl('./util/update_restart.sh', './util/update_restart.sh')

	return

