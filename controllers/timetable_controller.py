from __future__ import annotations
from typing import Union, Any, TYPE_CHECKING, Tuple

import psycopg2

from data_model.timetable import TimeTable
from flask import request, jsonify
from validators.timetable_validator import TimeTableValidator

from schedule_app import app

if TYPE_CHECKING:
    from flask import Response

validator = TimeTableValidator()


@app.route("/api/v1/timetable", methods=["GET"])
def get_timetable() -> Response:
    return jsonify([i.__dict__() for i in TimeTable.get_all(app.config.get("schedule_db_source"))])


@app.route("/api/v1/timetable/<int:object_id>", methods=["GET"])
def get_timetable_by_id(object_id: int) -> Response:
    return jsonify(TimeTable.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())


@app.route("/api/v1/timetable", methods=["POST"])
def create_timetable() -> Union[Response, Tuple[str, int]]:
    try:
        validator.validate(request.get_json(), "POST")
        return jsonify(TimeTable(**request.get_json(),
                                 db_source=app.config.get("schedule_db_source")).save().__dict__())
    except:
        return "", 400


@app.route("/api/v1/timetable/<int:object_id>", methods=["PUT"])
def update_timetable(object_id: int) -> Union[Tuple[str, int], Response]:
    if request.get_json().get('object_id') != object_id:
        return "", 400
    try:
        validator.validate(request.get_json(), "PUT")
    except:
        return "", 400
    try:
        TimeTable.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    return jsonify(TimeTable(**request.get_json(),
                             db_source=app.config.get("schedule_db_source")).save().__dict__())


@app.route("/api/v1/timetable/<int:object_id>", methods=["DELETE"])
def delete_timetable(object_id: int) -> Union[Response, Tuple[str, int], Tuple[Any, int]]:
    try:
        return jsonify(
            TimeTable.get_by_id(object_id, db_source=app.config.get("schedule_db_source")).delete().__dict__())
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400
