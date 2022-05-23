from __future__ import annotations
from data_model.teachers_for_subjects import TeachersForSubjects
from flask import jsonify, Response

from schedule_app import app


@app.route("/api/v1/teacher_for_subjects", methods=["GET"])
def get_teacher_for_subjects() -> Response:
    return jsonify([i.__dict__() for i in TeachersForSubjects.get_all(app.config.get("schedule_db_source"))])


@app.route("/api/v1/teacher_for_subjects/<int:object_id>", methods=["GET"])
def get_teacher_for_subjects_by_id(object_id: int) -> Response:
    return jsonify(TeachersForSubjects.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
