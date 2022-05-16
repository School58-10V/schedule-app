from flask import jsonify
from data_model.students_for_groups import StudentsForGroups

from schedule_app import app
dbf = app.config["db_factory"]


@app.route("/api/v1/students-for-groups", methods=["GET"])
def get_students_for_groups():
    return jsonify([i.__dict__() for i in StudentsForGroups.get_all(dbf.get_db_source())])


@app.route("/api/v1/students-for-groups/<object_id>", methods=["GET"])
def get_students_for_groups_by_id(object_id):
    try:
        return jsonify(StudentsForGroups.get_by_id(object_id, dbf.get_db_source()).__dict__())
    except ValueError:
        return "", 404

