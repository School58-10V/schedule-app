from __future__ import annotations
from typing import TYPE_CHECKING

import psycopg2, logging
from flask import request, jsonify


from schedule_app import app
from data_model.lesson import Lesson
from validators.lesson_validator import LessonValidator
from services.logger.messages_templates import MessagesTemplates

if TYPE_CHECKING:
    from flask import Response
    from typing import Union, Any, Tuple


validator = LessonValidator()
LOGGER = logging.getLogger("main.controller")
MESSAGES = MessagesTemplates()
MODEL = "Lesson"


@app.route("/api/v1/lesson", methods=["GET"])
def get_lessons() -> Union[Response, Tuple[str, int]]:
    try:
        data = [i.__dict__() for i in Lesson.get_all(app.config.get("schedule_db_source"))]
        LOGGER.info(MESSAGES.Controller.Success.get_collect_all_message(MODEL))
        return jsonify(data)
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_collect_all(MODEL))
        LOGGER.exception(err)
        return "", 500


@app.route("/api/v1/lesson/<int:object_id>", methods=["GET"])
def get_lesson_by_id(object_id: int) -> Union[Tuple[str, int], Response]:
    """
    :param object_id: int:
    :return json:
    """
    try:
        lesson_json = jsonify(Lesson.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
    except ValueError as e:
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
        LOGGER.exception(e)
        return '', 404
    LOGGER.info(MESSAGES.Controller.Success.get_find_by_id_message(MODEL, object_id))
    return lesson_json


@app.route("/api/v1/lesson", methods=["POST"])
def create_lesson() -> Union[Tuple[str, int], Response]:
    """
    :return json:
    """
    validation_data = validator.validate(request.get_json(), "POST")
    if not validation_data[0]:
        LOGGER.error(MESSAGES.General.get_validation_error_message(validation_data[1]))
        return validation_data[1], 400
    try:
        LOGGER.info(MESSAGES.Controller.Success.get_create_message(MODEL))
        return jsonify(Lesson(**request.get_json(), db_source=app.config.get("schedule_db_source"))
                       .save()
                       .__dict__())
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_create_message(MODEL))
        LOGGER.exception(err)
        return "", 500


@app.route("/api/v1/lesson/<int:object_id>", methods=["PUT"])
def update_lessons(object_id: int) -> Union[Tuple[str, int], Response]:
    """
    :param object_id: int:
    :return json:
    """
    if request.get_json().get('object_id') != object_id:
        LOGGER.error(MESSAGES.General.get_object_id_mismatch_message())
        return "", 400
    validation_data = validator.validate(request.get_json(), "PUT")
    if not validation_data[0]:
        LOGGER.warning(MESSAGES.General.get_validation_error_message(validation_data[1]))
        return validation_data[1], 400
    try:
        Lesson.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError as e:
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
        LOGGER.exception(e)
        return "", 404
    try:
        upd = Lesson(**request.get_json(), db_source=app.config.get("schedule_db_source")).save()
        LOGGER.info(MESSAGES.Controller.Success.get_update_message(MODEL))
        return jsonify(upd.__dict__())
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_update_message(MODEL))
        LOGGER.exception(err)
        return "", 500


@app.route("/api/v1/lesson/<int:object_id>", methods=["DELETE"])
def delete_lesson(object_id: int) -> Union[Union[Tuple[str, int], Tuple[Any, int]], Any]:
    """
    :param object_id: int:
    :return json:
    """
    try:
        lesson = Lesson.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError as e:
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
        LOGGER.exception(e)
        return "", 404
    try:
        lesson = lesson.delete().__dict__()
    except psycopg2.Error as e:
        LOGGER.error(MESSAGES.Controller.DBError.get_delete_message(MODEL, psycopg2.errorcodes.lookup(e.pgcode)))
        LOGGER.exception(e)
        return psycopg2.errorcodes.lookup(e.pgcode), 409
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_delete_message(MODEL))
        logging.exception(err)
        return "", 500
    return lesson
