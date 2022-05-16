import psycopg2

from data_model.teachers_for_subjects import TeachersForSubjects
from flask import jsonify

from schedule_app import app
dbf = app.config["db_factory"]


@app.route("/api/v1/teacher_for_subjects", methods=["GET"])
def get_teacher_for_subjects():
    return jsonify([i.__dict__() for i in TeachersForSubjects.get_all(dbf.get_db_source())])


@app.route("/api/v1/teacher_for_subjects/<object_id>", methods=["GET"])
def get_teacher_for_subjects_by_id(object_id):
    return jsonify(TeachersForSubjects.get_by_id(object_id, dbf.get_db_source()).__dict__())
