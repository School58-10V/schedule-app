import json
from data_model.lesson_row import LessonRow
from services.db_source_factory import DBFactory
from flask import Flask, request

app = Flask(__name__)
dbf = DBFactory()

# here will be your code


@app.route("/api/v1/lesson_row/<object_id>", methods=["PUT"])
def update_lesson_rows(object_id):
    try:
        LessonRow.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return LessonRow(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/lesson_row/<object_id>", methods=["DELETE"])
def delete_lesson_row(object_id):
    return {"method": "post"}