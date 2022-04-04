import json
import random

from flask import Flask, request

app = Flask(__name__)


@app.route("/home")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/post", methods=["POST"])
def hello_post():
    return {"method": "post"}


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return {"name": "main user"}
    if request.method == "POST":
        return {
            "status": "created",
            "name": json.loads(request.get_data().decode('utf8'))['name'],
        }


@app.route("/random_number", methods=["GET", "POST"])
def random_number():
    random_number_var = random.randint(0, 1000)
    if request.method.lower() == 'get':
        return f'<p>Случайное число от 0 до 1000!</p>\n' \
               f'<p>Барабанная дробь {random_number_var}</p>'
    elif request.method.lower() == 'post':
        return {'result': 'ok', 'data': {'number': random_number_var}}


if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
