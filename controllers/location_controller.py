from __future__ import annotations
from typing import TYPE_CHECKING

import logging, psycopg2
from flask import request, jsonify

from schedule_app import app
from data_model.location import Location
from validators.location_validator import LocationValidator

from services.logger.messages_templates import MessagesTemplates

if TYPE_CHECKING:
    from flask import Response
    from typing import Union, Any, Tuple


validator = LocationValidator()

LOGGER = logging.getLogger("main.controller")
MESSAGES = MessagesTemplates()
MODEL = "Location"

# here will be your code


@app.route("/api/v1/location/<int:object_id>", methods=['PUT'])
def update(object_id: int) -> Union[Tuple[str, int], Response]:
    """
    Обновляем Location
    :param object_id: int
    :return: Response
    """
    if request.get_json().get('object_id') != object_id:
        LOGGER.error(MESSAGES.General.get_object_id_mismatch_message())
        return "", 400
    validation_data = validator.validate(request.get_json(), "PUT")
    if not validation_data[0]:
        LOGGER.error(MESSAGES.General.get_validation_error_message(validation_data[1]))
        return validation_data[1], 400
    try:
        Location.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
        return "", 404
    try:
        LOGGER.info(MESSAGES.Controller.Success.get_update_message(MODEL))
        return jsonify(Location(**request.get_json(),
                                db_source=app.config.get("schedule_db_source")).save().__dict__())
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_update_message(MODEL))
        LOGGER.exception(err)
        return "", 500


@app.route("/api/v1/location", methods=["GET"])
def get_locations() -> Response | tuple[str, int]:
    """
        Выдаём все Locations
        :return: Response
        """
    try:
        data = [i.__dict__() for i in Location.get_all(app.config.get("schedule_db_source"))]
        LOGGER.info(MESSAGES.Controller.Success.get_collect_all_detailed_message(MODEL))
        return jsonify(data)
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_collect_all(MODEL))
        LOGGER.exception(err)
        return "", 500


@app.route("/api/v1/location/<int:object_id>", methods=["GET"])
def get_location_by_id(object_id: int) -> Union[Response, Tuple[str, int]]:
    """
    Выдаём Location по заданному id
    :param object_id: int
    :return: Response
    """
    try:
        data = Location.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
        LOGGER.info(MESSAGES.Controller.Success.get_find_by_id_message(MODEL, object_id))
        return jsonify(data)
    except ValueError:
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
        return '', 404


@app.route("/api/v1/location", methods=["POST"])
def create_location() -> Response():
    """
    Создаём Location по заданным аргументам
    :return: Response
    """
    validation_data = validator.validate(request.get_json(), "POST")
    if not validation_data[0]:
        LOGGER.error(MESSAGES.General.get_validation_error_message(validation_data[1]))
        return validation_data[1], 400
    try:
        data = Location(**request.get_json(), db_source=app.config.get("schedule_db_source")) \
                       .save().__dict__()
        LOGGER.info(MESSAGES.Controller.Success.get_create_message(MODEL))
        return jsonify(data)
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_create_message(MODEL))
        LOGGER.exception(err)
        return "", 500



@app.route("/api/v1/location/<int:object_id>", methods=["DELETE"])
def delete_location(object_id: int) -> Union[Tuple[str, int], Tuple[Any, int], Response]:
    """
    Удаляем Location по заданному id
    :param object_id: int
    :return: Response
    """
    try:
        location = Location.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
        return "", 404
    try:
        location = location.delete().__dict__()
    except psycopg2.Error as e:
        LOGGER.error(MESSAGES.Controller.DBError.get_delete_message(MODEL, psycopg2.errorcodes.lookup(e.pgcode)))
        LOGGER.exception(e)
        return psycopg2.errorcodes.lookup(e.pgcode), 409
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_delete_message(MODEL))
        LOGGER.exception(err)
        return "", 500
    LOGGER.info(MESSAGES.Controller.Success.get_delete_message(MODEL))
    return jsonify(location)
