import json

import psycopg2
from psycopg2 import errorcodes

from data_model.lesson_row import LessonRow
from services.db_source_factory import DBFactory
from flask import Flask, request

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/lesson-row", methods=["GET"])
def get_lesson_rows():
    return json.dumps([i.__dict__() for i in LessonRow.get_all(dbf.get_db_source())], ensure_ascii=False)


@app.route("/api/v1/lesson-row/<object_id>", methods=["GET"])
def get_lesson_row_by_id(object_id):
    try:
        return json.dumps(LessonRow.get_by_id(object_id, dbf.get_db_source()).__dict__(), ensure_ascii=False)
    except ValueError:
        return '', 404


@app.route("/api/v1/lesson-row", methods=["POST"])
def create_lesson_row():
    return LessonRow(**request.get_json(), db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/lesson-row/<object_id>", methods=["PUT"])
def update_lesson_rows(object_id):
    try:
        LessonRow.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return LessonRow(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/lesson-row/<object_id>", methods=["DELETE"])
def delete_lesson_row(object_id):
    print('tyt')
    try:
        lesson_row = LessonRow.get_by_id(object_id, dbf.get_db_source())
        lesson_row = lesson_row.delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        print(e)
        return errorcodes.lookup(e.pgcode), 409
    return lesson_row


# here will be your code

if __name__ == '__main__':
    app.run()
