import psycopg2

from flask import request, jsonify
from validators.timetable_validator import TimeTableValidator
from services.transformation_services.timetable_transformation_service import TimeTableTransformationService

from schedule_app import app

transform = TimeTableTransformationService()
validator = TimeTableValidator()
db_source = app.config.get("schedule_db_source")

@app.route("/api/v1/timetable", methods=["GET"])
def get_timetable():
    return jsonify(transform.get_timetable_transform(db_source))


@app.route("/api/v1/timetable/<object_id>", methods=["GET"])
def get_timetable_by_id(object_id):
    return jsonify(transform.get_timetable_by_id_transform(object_id, db_source))


@app.route("/api/v1/timetable", methods=["POST"])
def create_timetable():
    try:
        validator.validate(request.get_json(), "POST")
        return jsonify(transform.create_timetable_transform(request.get_json(), db_source))
    except ValueError:
        return "", 400

@app.route("/api/v1/timetable/<object_id>", methods=["PUT"])
def update_timetable(object_id):
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        return jsonify(transform.update_timetable_transform(object_id, request.get_json(), db_source))
    except ValueError:
        return "", 404


@app.route("/api/v1/timetable/<object_id>", methods=["DELETE"])
def delete_timetable(object_id):
    try:
        return jsonify(transform.delete_timetable_transform(object_id, db_source))
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400
