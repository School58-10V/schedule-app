import psycopg2

from data_model.timetable import TimeTable
from flask import request, jsonify

from schedule_app import app


@app.route("/api/v1/timetable", methods=["GET"])
def get_timetable():
    return jsonify([i.__dict__() for i in TimeTable.get_all(app.config.get("schedule_db_source"))])


@app.route("/api/v1/timetable/<object_id>", methods=["GET"])
def get_timetable_by_id(object_id):
    return jsonify(TimeTable.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())


@app.route("/api/v1/timetable", methods=["POST"])
def create_timetable():
    return jsonify(TimeTable(**request.get_json(),
                             db_source=app.config.get("schedule_db_source")).save().__dict__())


@app.route("/api/v1/timetable/<object_id>", methods=["PUT"])
def update_timetable(object_id):
    try:
        TimeTable.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    return jsonify(TimeTable(**request.get_json(), object_id=object_id,
                             db_source=app.config.get("schedule_db_source")).save().__dict__())


@app.route("/api/v1/timetable/<object_id>", methods=["DELETE"])
def delete_timetable(object_id):
    try:
        return jsonify(
            TimeTable.get_by_id(object_id, db_source=app.config.get("schedule_db_source")).delete().__dict__())
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400
