from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='templates')

# create anoter route for displaying files
@app.route('/')
def listBuilds():
	html_path = os.path.join(os.path.dirname(__file__), 'templates', 'fileList.html')
    # return the string that I want to send back to the browser
	directory = '/srv/ci'
	files = os.listdir(directory)
	return render_template('fileList.html', files=files)


@app.route("/<id>")
def show_build(id):
	headers = {'Content-Type': 'text/plain'}
	if not os.path.exists(f"/srv/ci/{id}"):
		return (f"Build with ID {id} not found", 404, headers)

	with open(f"/srv/ci/{id}", "r") as f:
		contents = f.read()
	return (contents, 200, headers)	