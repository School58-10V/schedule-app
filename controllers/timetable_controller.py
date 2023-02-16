from __future__ import annotations
from typing import TYPE_CHECKING

import psycopg2, logging
from flask import request, jsonify

from schedule_app import app
from data_model.timetable import TimeTable
from validators.timetable_validator import TimetableValidator

if TYPE_CHECKING:
    from flask import Response
    from typing import Union, Any, Tuple


validator = TimetableValidator()


@app.route("/api/v1/timetable", methods=["GET"])
def get_timetable() -> Response:
    try:
        return jsonify([i.__dict__() for i in TimeTable.get_all(app.config.get("schedule_db_source"))])
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/timetable/<int:object_id>", methods=["GET"])
def get_timetable_by_id(object_id) -> Response:
    try:
        return jsonify(TimeTable.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
    except ValueError:
        return "", 404


@app.route("/api/v1/timetable/current", methods=["GET"])
def get_current_timetable() -> Response:
    try:
        return jsonify(TimeTable.get_current_timetable(app.config.get("schedule_db_source")))
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/timetable", methods=["POST"])
def create_timetable() -> Union[Response, Tuple[str, int]]:
    validation_data = validator.validate(request.get_json(), "POST")
    if not validation_data[0]:
        return validation_data[1], 400
    try:
        return jsonify(TimeTable(**request.get_json(),
                                 db_source=app.config.get("schedule_db_source")).save().__dict__())
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500



@app.route("/api/v1/timetable/<int:object_id>", methods=["PUT"])
def update_timetable(object_id: int) -> Union[Tuple[str, int], Response]:
    if request.get_json().get('object_id') != object_id:
        return "", 400
    validation_data = validator.validate(request.get_json(), "PUT")
    if (not validation_data[0]):
        return validation_data[1], 400
    try:
        TimeTable.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        return jsonify(TimeTable(**request.get_json(),
                                 db_source=app.config.get("schedule_db_source")).save().__dict__())
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/timetable/<int:object_id>", methods=["DELETE"])
def delete_timetable(object_id: int) -> Union[Response, Tuple[str, int], Tuple[Any, int]]:
    try:
        timetable = TimeTable.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        timetable = timetable.delete().__dict__()
        return jsonify(timetable)
    except psycopg2.Error as e:
        return jsonify(psycopg2.errorcodes.lookup(e.pgcode)), 409
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500
