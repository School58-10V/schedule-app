from typing import Union, Any

import psycopg2
from psycopg2 import errorcodes

from data_model.lesson import Lesson
from validators.lesson_validator import LessonValidator
from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify, Response

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/lesson", methods=["GET"])
def get_lessons() -> Response:
    """
    :return json:
    """
    return jsonify([i.__dict__() for i in Lesson.get_all(dbf.get_db_source())])


@app.route("/api/v1/lesson/<object_id>", methods=["GET"])
def get_lesson_by_id(object_id: int) -> Union[tuple[str, int], Response]:
    """
    :param object_id: int:
    :return json:
    """
    try:
        lesson_json = jsonify(Lesson.get_by_id(object_id, dbf.get_db_source()).__dict__())
    except ValueError:
        return '', 404
    return lesson_json


@app.route("/api/v1/lesson", methods=["POST"])
def create_lesson() -> Response:
    """
    :return json:
    """
    request_validator = LessonValidator()
    try:
        request_validator.validate(request.get_json(), 'POST')
        return jsonify(Lesson(**request.get_json
        (), db_source=dbf.get_db_source())
                       .save()
                       .__dict__())
    except ValueError:
        return '', 400


@app.route("/api/v1/lesson/<object_id>", methods=["PUT"])
def update_lessons(object_id: int) -> Union[tuple[str, int], Response]:
    """
    :param object_id: int:
    :return json:
    """
    request_validator = LessonValidator()
    try:
        request_validator.validate(request.get_json(), 'PUT')
        Lesson.get_by_id(object_id, db_source=dbf.get_db_source())
        return jsonify(Lesson(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source())
                       .save()
                       .__dict__())
    except ValueError:
        return "", 404


@app.route("/api/v1/lesson/<object_id>", methods=["DELETE"])
def delete_lesson(object_id: int) -> Union[Union[tuple[str, int], tuple[Any, int]], Any]:
    """
    :param object_id: int:
    :return json:
    """
    try:
        lesson = Lesson.get_by_id(object_id, dbf.get_db_source())
        lesson = lesson.delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        print(e)
        return errorcodes.lookup(e.pgcode), 409
    return lesson


if __name__ == '__main__':
    app.run()
