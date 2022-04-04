import json
from flask import Flask, request


app = Flask(__name__)


@app.route("/home")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/post", methods=["POST"])
def hello_post():
    return { "method": "post" }


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return { "name": "main user" }
    if request.method == "POST":
        return {
            "status": "created",
            "name": json.loads(request.get_data().decode('utf8'))['name'],
        }
