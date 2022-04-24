import psycopg2

from data_model.teacher import Teacher
from data_model.teachers_for_subjects import TeachersForSubjects
from data_model.teachers_for_lesson_rows import TeachersForLessonRows

from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/teachers", methods=["GET"])
def get_teachers():
    teachers = []
    for i in Teacher.get_all(dbf.get_db_source()):
        teacher = i.__dict__()
        teacher['subject_id'] = [j.get_main_id() for j in TeachersForSubjects.
            get_subjects_by_teacher_id(i.get_main_id(), db_source=dbf.get_db_source())]
        teacher['lesson_row_id'] = [j.get_main_id() for j in TeachersForLessonRows.
            get_lesson_rows_by_teacher_id(i.get_main_id(), db_source=dbf.get_db_source())]
        teachers.append(teacher)
    return jsonify({"teachers": teachers})


@app.route("/api/v1/teachers/<object_id>", methods=["GET"])
def get_teacher_by_id(object_id):
    try:
        teacher = Teacher.get_by_id(object_id, dbf.get_db_source()).__dict__()
        teacher['subject_id'] = [i.get_main_id() for i in TeachersForSubjects.
            get_subjects_by_teacher_id(object_id, db_source=dbf.get_db_source())]
        teacher['lesson_row_id'] = [i.get_main_id() for i in TeachersForLessonRows.
            get_lesson_rows_by_teacher_id(object_id, db_source=dbf.get_db_source())]
        return teacher
    except ValueError:
        return '', 404


@app.route("/api/v1/teachers/get/detailed", methods=["GET"])
def get_detailed_teachers():
    teachers = []
    for i in Teacher.get_all(dbf.get_db_source()):
        object_id = i.get_main_id()
        teacher = Teacher.get_by_id(object_id, dbf.get_db_source()).__dict__()
        teacher['subject'] = [i.__dict__() for i in TeachersForSubjects.
            get_subjects_by_teacher_id(object_id, db_source=dbf.get_db_source())]
        teacher['lesson_row'] = [i.__dict__() for i in TeachersForLessonRows.
            get_lesson_rows_by_teacher_id(object_id, db_source=dbf.get_db_source())]
        teachers.append(teacher)
    return jsonify({"teachers": teachers})


@app.route("/api/v1/teachers/get/detailed/<object_id>", methods=["GET"])
def get_teacher_detailed_by_id(object_id):
    try:
        teacher = Teacher.get_by_id(object_id, dbf.get_db_source()).__dict__()
        teacher['subject_id'] = [i.__dict__() for i in TeachersForSubjects.
            get_subjects_by_teacher_id(object_id, db_source=dbf.get_db_source())]
        teacher['lesson_row_id'] = [i.__dict__() for i in TeachersForLessonRows.
            get_lesson_rows_by_teacher_id(object_id, db_source=dbf.get_db_source())]
        return teacher
    except ValueError:
        return '', 404


@app.route("/api/v1/teachers", methods=["POST"])
def create_teacher():
    try:
        subject_id = request.get_json()['subject_id']
        lesson_row_id = request.get_json()['lesson_row_id']
        dct = request.get_json()
        del dct['subject_id']
        del dct['lesson_row_id']

        new_teacher = Teacher(**dct, db_source=dbf.get_db_source()).save()

        for i in subject_id:
            TeachersForSubjects(teacher_id=new_teacher.get_main_id(), subject_id=i, db_source=dbf.get_db_source()).save()

        for i in lesson_row_id:
            TeachersForLessonRows(teacher_id=new_teacher.get_main_id(), lesson_row_id=i, db_source=dbf.get_db_source()).save()

        return Teacher.get_by_id(element_id=new_teacher.__dict__()['object_id'], db_source=dbf.get_db_source())

    except TypeError:
        return '', 400


@app.route("/api/v1/teachers/<object_id>", methods=["PUT"])
def update_teacher(object_id):
    try:
        teacher = Teacher.get_by_id(object_id, dbf.get_db_source()).__dict__()
        teacher.update(request.get_json())
        return jsonify(Teacher(**teacher, db_source=dbf.get_db_source()).save().__dict__())
    except ValueError:
        return '', 404
    except TypeError:
        return '', 400


@app.route("/api/v1/teachers/<object_id>", methods=["DELETE"])
def delete_teacher(object_id):
    try:
        return Teacher.get_by_id(object_id, dbf.get_db_source()).delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400

      
if __name__ == '__main__':
    app.run()
