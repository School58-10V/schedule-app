import json
from data_model.timetable import TimeTable
from services.db_source_factory import DBFactory
from flask import Flask, request

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/timetable", methods=["GET"])
def get_timetable():
    return json.dumps([i.__dict__() for i in TimeTable.get_all(dbf.get_db_source())], ensure_ascii=False)


@app.route("/api/v1/timetable/<object_id>", methods=["GET"])
def get_timetable_by_id(object_id):
    return json.dumps(TimeTable.get_by_id(object_id, dbf.get_db_source()).__dict__(), ensure_ascii=False)


@app.route("/api/v1/timetable", methods=["POST"])
def create_timetable():
    return TimeTable(**request.get_json(), db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/timetable/<object_id>", methods=["PUT"])
def update_timetable(object_id):
    try:
        TimeTable.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return TimeTable(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/timetable/<object_id>", methods=["DELETE"])
def delete_timetable(object_id):
    if request.method == 'DELETE':
        return TimeTable.get_by_id(object_id, db_source=dbf.get_db_source()).delete().__dict__()


if __name__ == '__main__':
    app.run()
