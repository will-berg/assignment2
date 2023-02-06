from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle():
	print(request.data)
