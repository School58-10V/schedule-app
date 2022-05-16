import psycopg2

from data_model.timetable import TimeTable
from validators.timetable_validator import TimeTableValidator
from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/timetable", methods=["GET"])
def get_timetable():
    return jsonify([i.__dict__() for i in TimeTable.get_all(dbf.get_db_source())])


@app.route("/api/v1/timetable/<object_id>", methods=["GET"])
def get_timetable_by_id(object_id):
    return jsonify(TimeTable.get_by_id(object_id, dbf.get_db_source()).__dict__())


@app.route("/api/v1/timetable", methods=["POST"])
def create_timetable():
    request_validator = TimeTableValidator()
    request_validator.validate(request.get_json(), 'POST')
    return jsonify(TimeTable(**request.get_json(), db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()
                   )


@app.route("/api/v1/timetable/<object_id>", methods=["PUT"])
def update_timetable(object_id):
    try:
        request_validator = TimeTableValidator()
        request_validator.validate(request.get_json(), 'PUT')
        TimeTable.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return jsonify(TimeTable(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()
                   )


@app.route("/api/v1/timetable/<object_id>", methods=["DELETE"])
def delete_timetable(object_id):
    try:
        return jsonify(TimeTable.get_by_id(object_id, db_source=dbf.get_db_source()).delete().__dict__())
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400


if __name__ == '__main__':
    app.run()
