from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from flask import jsonify

from schedule_app import app
dbf = app.config["db_factory"]


@app.route("/api/v1/teacher_for_lesson_rows", methods=["GET"])
def get_teacher_for_lesson_rows():
    return jsonify([i.__dict__() for i in TeachersForLessonRows.get_all(dbf.get_db_source())])


@app.route("/api/v1/teacher_for_lesson_rows/<object_id>", methods=["GET"])
def get_teacher_for_lesson_rows_by_id(object_id):
    try:
        return jsonify(TeachersForLessonRows.get_by_id(object_id, dbf.get_db_source()).__dict__())
    except ValueError:
        return '', 404
