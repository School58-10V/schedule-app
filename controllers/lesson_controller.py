from __future__ import annotations
from typing import TYPE_CHECKING

import psycopg2, logging
from flask import request, jsonify


from schedule_app import app
from data_model.lesson import Lesson
from validators.lesson_validator import LessonValidator

if TYPE_CHECKING:
    from flask import Response
    from typing import Union, Any, Tuple


validator = LessonValidator()


@app.route("/api/v1/lesson", methods=["GET"])
def get_lessons() -> Union[Response, Tuple[str, int]]:
    try:
        return jsonify([i.__dict__() for i in Lesson.get_all(app.config.get("schedule_db_source"))])
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


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
    except ValueError:
        return "", 400
    try:
        return jsonify(Lesson(**request.get_json(), source=app.config.get("schedule_db_source"))
                       .save()
                       .__dict__())
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


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
        Lesson.get_by_id(object_id, source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        return jsonify(Lesson(**request.get_json(), source=app.config.get("schedule_db_source"))
                       .save()
                       .__dict__())
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/lesson/<int:object_id>", methods=["DELETE"])
def delete_lesson(object_id: int) -> Union[Union[Tuple[str, int], Tuple[Any, int]], Any]:
    """
    :param object_id: int:
    :return json:
    """
    try:
        lesson = Lesson.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        lesson = lesson.delete().__dict__()
    except psycopg2.Error as e:
        print(e)
        return psycopg2.errorcodes.lookup(e.pgcode), 409
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500
    return lesson
