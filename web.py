from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='templates')

# create anoter route for displaying files
@app.route('/')
def listBuilds():
	directory = os.environ['BUILD_OUTPUT']
	files = os.listdir(directory)
	return render_template('fileList.html', files=files)


@app.route("/<id>")
def show_build(id):
	directory = os.environ['BUILD_OUTPUT']
	headers = {'Content-Type': 'text/plain'}
	if not os.path.exists(f"{directory}/{id}"):
		return (f"Build with ID {id} not found", 404, headers)

	with open(f"{directory}/{id}", "r") as f:
		contents = f.read()
	return (contents, 200, headers)