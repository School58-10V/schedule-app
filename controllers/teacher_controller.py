import psycopg2

from data_model.teacher import Teacher
from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify
from data_model.teachers_for_subjects import TeachersForSubjects
from data_model.teachers_for_lesson_rows import TeachersForLessonRows

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/teacher", methods=["GET"])
def get_teachers():
    return jsonify([i.__dict__() for i in Teacher.get_all(dbf.get_db_source())])


@app.route("/api/v1/teacher/<object_id>", methods=["GET"])
def get_teacher_by_id(object_id):
    try:
        return jsonify(Teacher.get_by_id(object_id, dbf.get_db_source()).__dict__())
    except ValueError:
        return '', 404


@app.route("/api/v1/teacher", methods=["POST"])
def create_teacher():
    try:
        return Teacher(**request.get_json(), db_source=dbf.get_db_source()).save().__dict__()
    except TypeError:
        return '', 400


@app.route("/api/v1/teacher/<object_id>", methods=["PUT"])
def update_teacher(object_id):
    try:
        teacher = Teacher.get_by_id(object_id, dbf.get_db_source()).__dict__()
        teacher.update(request.get_json())
        return jsonify(Teacher(**teacher, db_source=dbf.get_db_source()).save().__dict__())
    except ValueError:
        return '', 404
    except TypeError:
        return '', 400


@app.route("/api/v1/teacher/<object_id>", methods=["DELETE"])
def delete_teacher(object_id):
    try:
        return Teacher.get_by_id(object_id, dbf.get_db_source()).delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400


@app.route("/api/v1/teacher/get_subjects/<object_id>", methods=["GET"])
def get_subjects(object_id):
    try:
        dct = Teacher.get_by_id(object_id, dbf.get_db_source()).__dict__()
        dct['subject_id'] = [i.get_main_id() for i in TeachersForSubjects.
            get_subjects_by_teacher_id(object_id, db_source=dbf.get_db_source())]
        return jsonify(dct['subject_id'])
    except ValueError:
        return '', 404


@app.route("/api/v1/teacher/get_lesson_rows/<object_id>", methods=["GET"])
def get_lesson_rows(object_id):
    try:
        dct = Teacher.get_by_id(object_id, dbf.get_db_source()).__dict__()
        dct['lesson_row_id'] = [i.get_main_id() for i in TeachersForLessonRows.
            get_lesson_rows_by_teacher_id(object_id, db_source=dbf.get_db_source())]
        return jsonify(dct['lesson_row_id'])
    except ValueError:
        return '', 404


if __name__ == '__main__':
    app.run()
