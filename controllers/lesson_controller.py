import json
from data_model.lesson import Lesson
from services.db_source_factory import DBFactory
from flask import Flask, request

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/lesson", methods=["POST"])
def create_lesson():
    return Lesson(**request.get_json(), db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/lesson/<object_id>", methods=["PUT"])
def update_lessons(object_id):
    try:
        Lesson.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return Lesson(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/lesson/<object_id>", methods=["DELETE"])
def delete_lesson(object_id):
    return {"method": "post"}


if __name__ == '__main__':
    app.run()
