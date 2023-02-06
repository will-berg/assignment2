from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def update():
	if not request.headers.get('User-Agent').startswith('GitHub-Hookshot'):
		return ({'message': 'Only GitHub can call this endpoint.'}, 403)

	event = request.headers.get('X-GitHub-Event')

	if event is None:
		return ({'message': 'The event type wasn\'t specified.'}, 400)

	if event == 'push':
		return ({'message': 'This event is currently unimplemented.'}, 501)
	elif event == 'ping':
		return ({}, 200)
	else:
		return ({'message': f'Event {event} is not supported.'}, 400)