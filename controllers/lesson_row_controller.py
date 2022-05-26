from __future__ import annotations
from typing import TYPE_CHECKING, Union
import psycopg2
from psycopg2 import errorcodes
from flask import request, jsonify
from validators.lesson_row_validator import LessonRowValidator
from services.transformation_services.lesson_row_transformation_service import LessonRowTransformationService


if TYPE_CHECKING:
    from flask import Response

from schedule_app import app

validator = LessonRowValidator()
transform = LessonRowTransformationService()
db_source = app.config.get("schedule_db_source")

@app.route("/api/v1/lesson-row", methods=["GET"])
def get_all_lesson_rows() -> Response:
    """
    Достаем все LessonRow
    :return: Response
    """
    return jsonify(transform.get_all_lesson_rows_transform(db_source))


@app.route('/api/v1/lesson-row/detailed', methods=["GET"])
def get_all_detailed() -> Response:
    """
    Достаем все LessonRow вместе с учителями
    :return: Response
    """
    return jsonify(transform.get_all_detailed_transform(db_source))


@app.route("/api/v1/lesson-row/<object_id>", methods=["GET"])
def get_lesson_row_by_id(object_id: int) -> Union[Response, tuple[str, int]]:
    """
    Достаем LessonRow по id
    :param object_id: int
    :return: Response
    """
    try:
        return jsonify(transform.get_lesson_row_by_id_transform(object_id, db_source))
    except ValueError:
        return '', 404


@app.route('/api/v1/lesson-row/detailed/<object_id>', methods=['GET'])
def get_detailed_lesson_row_by_id(object_id: int) -> Union[Response, tuple[str, int]]:
    """
    Дастаем LessonRow по id вместе с учителями
    :param object_id: int
    :return: Response
    """
    try:
        return jsonify(transform.get_detailed_lesson_row_by_id_transform(object_id, db_source))
    except ValueError:
        return '', 404


@app.route("/api/v1/lesson-row", methods=["POST"])
def create_lesson_row() -> Union[Response, tuple[str, int]]:
    """
    Создаем LessonRow
    :return: Response
    """
    try:
        validator.validate(request.get_json(), "POST")
    except ValueError:
        return '', 400
    try:
        return jsonify(transform.create_lesson_row_transform(request.get_json(), db_source))
    except TypeError:
        return '', 400
    except ValueError:
        return '', 401


@app.route("/api/v1/lesson-row/<object_id>", methods=["PUT"])
def update_lesson_rows(object_id: int) -> Union[Response, tuple[str, int]]:
    """
    Обновляем LessonRow по данному id
    :param object_id:
    :return: Response
    """
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        transform.check_availability(object_id)
        return transform.update_lesson_rows_transform(object_id, request.get_json(), db_source)
    except ValueError:
        return "", 404


@app.route("/api/v1/lesson-row/<object_id>", methods=["DELETE"])
def delete_lesson_row(object_id: int) -> Union[Response, tuple[str, int]]:
    """
    Удаляем LessonRow по данному id
    :param object_id: int
    :return: Response
    """
    try:
        return jsonify(transform.delete_lesson_row_transform(object_id, db_source))
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        print(e)
        return jsonify(errorcodes.lookup(e.pgcode), 409)
