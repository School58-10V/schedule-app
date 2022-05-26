from typing import Union, Any, Tuple
import psycopg2
from validators.lesson_validator import LessonValidator
from psycopg2 import errorcodes
from data_model.lesson import Lesson
from flask import request, jsonify, Response

from schedule_app import app

validator = LessonValidator()


@app.route("/api/v1/lesson", methods=["GET"])
def get_lessons() -> Response:
    """
    :return json:
    """
    return jsonify([i.__dict__() for i in Lesson.get_all(app.config.get("schedule_db_source"))])


@app.route("/api/v1/lesson/<int:object_id>", methods=["GET"])
def get_lesson_by_id(object_id: int) -> Union[Tuple[str, int], Response]:
    """
    :param object_id: int:
    :return json:
    """
    try:
        lesson_json = jsonify(Lesson.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
    except ValueError:
        return '', 404
    return lesson_json


@app.route("/api/v1/lesson", methods=["POST"])
def create_lesson() -> Union[Tuple[str, int], Response]:
    """
    :return json:
    """
    try:
        validator.validate(request.get_json(), "POST")
        return jsonify(Lesson(**request.get_json(), db_source=app.config.get("schedule_db_source"))
                       .save()
                       .__dict__())
    except ValueError:
        return "", 400


@app.route("/api/v1/lesson/<int:object_id>", methods=["PUT"])
def update_lessons(object_id: int) -> Union[Tuple[str, int], Response]:
    """
    :param object_id: int:
    :return json:
    """
    if request.get_json().get('object_id') != object_id:
        return "", 400
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        Lesson.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    return jsonify(Lesson(**request.get_json(), db_source=app.config.get("schedule_db_source"))
                   .save()
                   .__dict__())


@app.route("/api/v1/lesson/<int:object_id>", methods=["DELETE"])
def delete_lesson(object_id: int) -> Union[Union[Tuple[str, int], Tuple[Any, int]], Any]:
    """
    :param object_id: int:
    :return json:
    """
    try:
        lesson = Lesson.get_by_id(object_id, app.config.get("schedule_db_source"))
        lesson = lesson.delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        print(e)
        return errorcodes.lookup(e.pgcode), 409
    return jsonify(lesson)
