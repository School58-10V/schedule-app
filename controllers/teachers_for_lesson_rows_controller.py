from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from services.db_source_factory import DBFactory
from flask import Flask, jsonify

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/teacher_for_lesson_rows", methods=["GET"])
def get_teacher_for_lesson_rows():
    return jsonify([i.__dict__() for i in TeachersForLessonRows.get_all(dbf.get_db_source())])


@app.route("/api/v1/teacher_for_lesson_rows/<object_id>", methods=["GET"])
def get_teacher_for_lesson_rows_by_id(object_id):
    try:
        return jsonify(TeachersForLessonRows.get_by_id(object_id, dbf.get_db_source()).__dict__())
    except:
        return '', 404


if __name__ == '__main__':
    app.run()
