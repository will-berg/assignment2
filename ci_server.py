from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle():
	if not request.headers.get('User-Agent').startswith('GitHub-Hookshot'):
		return ({'message': 'Only GitHub can call this endpoint.'}, 403)

	event = request.headers.get('X-GitHub-Event')

	if event == 'ping':
		return ({'message': 'We are here \o/'}, 200)
