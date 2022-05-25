import logging

import psycopg2
from psycopg2 import errorcodes
from data_model.timetable import TimeTable
from flask import request, jsonify
from validators.timetable_validator import TimeTableValidator

from schedule_app import app

validator = TimeTableValidator()


@app.route("/api/v1/timetable", methods=["GET"])
def get_timetable():
    try:
        return jsonify([i.__dict__() for i in TimeTable.get_all(app.config.get("schedule_db_source"))])
    except Exception as err:
        logging.error(err)
        return "", 500


@app.route("/api/v1/timetable/<object_id>", methods=["GET"])
def get_timetable_by_id(object_id):
    try:
        return jsonify(TimeTable.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
    except ValueError:
        return "", 404


@app.route("/api/v1/timetable", methods=["POST"])
def create_timetable():
    try:
        validator.validate(request.get_json(), "POST")
    except ValueError:
        return "", 400
    try:
        return jsonify(TimeTable(**request.get_json(),
                                 db_source=app.config.get("schedule_db_source")).save().__dict__())
    except Exception as err:
        logging.error(err)
        return "", 500


@app.route("/api/v1/timetable/<object_id>", methods=["PUT"])
def update_timetable(object_id):
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        TimeTable.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        return jsonify(TimeTable(**request.get_json(), object_id=object_id,
                                 db_source=app.config.get("schedule_db_source")).save().__dict__())
    except Exception as err:
        logging.error(err)
        return "", 500


@app.route("/api/v1/timetable/<object_id>", methods=["DELETE"])
def delete_timetable(object_id):
    try:
        timetable = TimeTable.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        timetable = timetable.delete().__dict__()
        return jsonify(timetable)
    except psycopg2.Error as e:
        return jsonify(errorcodes.lookup(e.pgcode)), 409
    except Exception as err:
        logging.error(err)
        return "", 500
