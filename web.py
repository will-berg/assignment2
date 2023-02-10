"""
Displays build information on web pages. Each build is given a unique URL using its
commit identifier. At the root of the web page, all builds are listed as links to
their respective CI output web pages.
"""
from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='templates')

# Lists all builds as URLs to their CI output web pages, viewable at URL http://molly.aronbergman.se/
@app.route('/')
def listBuilds():
	directory = os.environ['BUILD_OUTPUT']
	files = os.listdir(directory)
	return render_template('fileList.html', files=files)


# Displays the CI outputs of a build at the URL http://molly.aronbergman.se/id, where id is the commit id
@app.route("/<id>")
def show_build(id):
	directory = os.environ['BUILD_OUTPUT']
	headers = {'Content-Type': 'text/plain'}
	if not os.path.exists(f"{directory}/{id}"):
		return (f"Build with ID {id} not found", 404, headers)

	with open(f"{directory}/{id}", "r") as f:
		contents = f.read()
	return (contents, 200, headers)