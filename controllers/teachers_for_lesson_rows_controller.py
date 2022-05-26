import logging

from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from flask import jsonify

from schedule_app import app


@app.route("/api/v1/teacher_for_lesson_rows", methods=["GET"])
def get_teacher_for_lesson_rows():
    try:
        return jsonify([i.__dict__() for i in TeachersForLessonRows.get_all(app.config.get("schedule_db_source"))])
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/teacher_for_lesson_rows/<object_id>", methods=["GET"])
def get_teacher_for_lesson_rows_by_id(object_id):
    try:
        return jsonify(TeachersForLessonRows.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
    except ValueError:
        return '', 404
