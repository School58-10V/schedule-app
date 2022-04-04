import json
from flask import Flask, request

from data_model.student import Student
from db_source import DBSource

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


a = DBSource(user='schedule_app', password='VYRL!9XEB3yXQs4aPz_Q', host='postgresql.aakapustin.ru')


@app.route('/name', methods=['GET', 'POST'])
def get_name():
    if request.method == 'GET':
        return {i.get_main_id(): i.get_full_name() for i in Student.get_all(db_source=a)}
    # if request.method



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
