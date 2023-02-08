from flask import Flask
import os

app = Flask(__name__)

@app.route("/<id>")
def show_build(id):
	headers = {'Content-Type': 'text/plain'}
	if not os.path.exists(f"/srv/ci/{id}"):
		return (f"Build with ID {id} not found", 404, headers)

	with open(f"/srv/ci/{id}", "r") as f:
		contents = f.read()
	return (contents, 200, headers)