import json
from data_model.lesson import Lesson
from services.db_source_factory import DBFactory
from flask import Flask, request

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/lesson", methods=["GET"])
def get_lessons():
    return json.dumps([i.__dict__() for i in Lesson.get_all(dbf.get_db_source())], ensure_ascii=False)


@app.route("/api/v1/lesson/<object_id>", methods=["GET"])
def get_lesson_by_id(object_id):
    return json.dumps(Lesson.get_by_id(object_id, dbf.get_db_source()).__dict__(), ensure_ascii=False)
