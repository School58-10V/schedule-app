from typing import Union, Any, Tuple
import psycopg2
from validators.lesson_validator import LessonValidator
from psycopg2 import errorcodes
from services.transformation_services.lesson_transformation_service import LessonTransformationService
from flask import request, jsonify, Response

from schedule_app import app

transform = LessonTransformationService()
validator = LessonValidator()

@app.route("/api/v1/lesson", methods=["GET"])
def get_lessons() -> Response:
    """
    :return json:
    """
    return jsonify(transform.get_lessons_trasform())


@app.route("/api/v1/lesson/<object_id>", methods=["GET"])
def get_lesson_by_id(object_id: int) -> Union[Tuple[str, int], Response]:
    """
    :param object_id: int:
    :return json:
    """
    try:
        return transform.get_lesson_by_id_transform(object_id)
    except ValueError:
        return '', 404


@app.route("/api/v1/lesson", methods=["POST"])
def create_lesson() -> Union[Tuple[str, int], Response]:
    """
    :return json:
    """
    try:
        validator.validate(request.get_json(), "POST")
        return jsonify(transform.create_lesson_transform(request.get_json()))
    except ValueError:
        return "", 400


@app.route("/api/v1/lesson/<object_id>", methods=["PUT"])
def update_lessons(object_id: int) -> Union[Tuple[str, int], Response]:
    """
    :param object_id: int:
    :return json:
    """
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        return jsonify(transform.update_lessons_transform(object_id, request.get_json()))
    except ValueError:
        return "", 404


@app.route("/api/v1/lesson/<object_id>", methods=["DELETE"])
def delete_lesson(object_id: int) -> Union[Union[Tuple[str, int], Tuple[Any, int]], Any]:
    """
    :param object_id: int:
    :return json:
    """
    try:
        return transform.delete_lesson_transform(object_id)
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        print(e)
        return errorcodes.lookup(e.pgcode), 409
