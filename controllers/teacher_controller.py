import logging

import psycopg2
from psycopg2 import errorcodes
from data_model.teacher import Teacher
from data_model.teachers_for_subjects import TeachersForSubjects
from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from validators.teacher_validator import TeacherValidator
from flask import request, jsonify

from schedule_app import app

validator = TeacherValidator()


@app.route("/api/v1/teachers", methods=["GET"])
def get_teachers():
    try:
        teachers = []
        for i in Teacher.get_all(app.config.get("schedule_db_source")):
            teacher = i.__dict__()
            teacher['subject_id'] = [j.get_main_id() for j in TeachersForSubjects.
                get_subjects_by_teacher_id(i.get_main_id(),
                                           db_source=app.config.get("schedule_db_source"))]
            teacher['lesson_row_id'] = [j.get_main_id() for j in TeachersForLessonRows.
                get_lesson_rows_by_teacher_id(i.get_main_id(),
                                              db_source=app.config.get("schedule_db_source"))]
            teachers.append(teacher)
        return jsonify({"teachers": teachers})
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/teachers/<object_id>", methods=["GET"])
def get_teacher_by_id(object_id):
    try:

        teacher = Teacher.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
        teacher['subject_id'] = [i.get_main_id() for i in TeachersForSubjects.
            get_subjects_by_teacher_id(object_id,
                                       db_source=app.config.get("schedule_db_source"))]
        teacher['lesson_row_id'] = [i.get_main_id() for i in TeachersForLessonRows.
            get_lesson_rows_by_teacher_id(object_id,
                                          db_source=app.config.get("schedule_db_source"))]
        return jsonify(teacher)
    except ValueError:
        return '', 404


@app.route("/api/v1/teachers/get/detailed", methods=["GET"])
def get_detailed_teachers():
    try:
        teachers = []
        for i in Teacher.get_all(app.config.get("schedule_db_source")):
            object_id = i.get_main_id()
            teacher = Teacher.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
            teacher['subject'] = [i.__dict__() for i in TeachersForSubjects.
                get_subjects_by_teacher_id(object_id,
                                           db_source=app.config.get("schedule_db_source"))]
            teacher['lesson_row'] = [i.__dict__() for i in TeachersForLessonRows.
                get_lesson_rows_by_teacher_id(object_id,
                                              db_source=app.config.get("schedule_db_source"))]
            teachers.append(teacher)
        return jsonify({"teachers": teachers})
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/teachers/get/detailed/<object_id>", methods=["GET"])
def get_teacher_detailed_by_id(object_id):
    try:
        teacher = Teacher.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
        teacher['subject_id'] = [i.__dict__() for i in TeachersForSubjects.
            get_subjects_by_teacher_id(object_id,
                                       db_source=app.config.get("schedule_db_source"))]
        teacher['lesson_row_id'] = [i.__dict__() for i in TeachersForLessonRows.
            get_lesson_rows_by_teacher_id(object_id,
                                          db_source=app.config.get("schedule_db_source"))]
        return teacher
    except ValueError:
        return '', 404


@app.route("/api/v1/teachers", methods=["POST"])
def create_teacher():
    dct = request.get_json()
    try:
        validator.validate(dct, "POST")
    except:
        return '', 400
    try:
        subject_id = dct.pop('subject_id')
        lesson_row_id = dct.pop('lesson_row_id')

        new_teacher = Teacher(**dct, db_source=app.config.get("schedule_db_source")).save()

        for i in subject_id:
            TeachersForSubjects(teacher_id=new_teacher.get_main_id(), subject_id=i,
                                db_source=app.config.get("schedule_db_source")).save()

        for i in lesson_row_id:
            TeachersForLessonRows(teacher_id=new_teacher.get_main_id(), lesson_row_id=i,
                                  db_source=app.config.get("schedule_db_source")).save()

        new_teacher_dct = new_teacher.__dict__()
        new_teacher_dct['subject_id'] = subject_id
        new_teacher_dct['lesson_row_id'] = lesson_row_id

        return jsonify(new_teacher_dct)
    except ValueError:
        return '', 404
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/teachers/<object_id>", methods=["PUT"])
def update_teacher(object_id):
    try:
        validator.validate(request.get_json(), "PUT")
    except:
        return "", 400
    try:
        teacher = Teacher.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
    except ValueError:
        return "", 404
    try:
        teacher['subject_id'] = [i.get_main_id() for i in TeachersForSubjects.
            get_subjects_by_teacher_id(object_id, db_source=app.config.get("schedule_db_source"))]
        teacher['lesson_row_id'] = [i.get_main_id() for i in TeachersForLessonRows.
            get_lesson_rows_by_teacher_id(object_id,
                                          db_source=app.config.get("schedule_db_source"))]

        for i in request.get_json()['subject_id']:
            if i not in teacher['subject_id']:
                TeachersForSubjects(teacher_id=object_id, subject_id=i,
                                    db_source=app.config.get("schedule_db_source")).save()

        for i in request.get_json()['lesson_row_id']:
            if i not in teacher['lesson_row_id']:
                TeachersForLessonRows(teacher_id=object_id, lesson_row_id=i,
                                      db_source=app.config.get("schedule_db_source")).save()

        return jsonify(Teacher.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/teachers/<object_id>", methods=["DELETE"])
def delete_teacher(object_id):
    try:
        teacher = Teacher.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        teacher = teacher.delete().__dict__()
        return jsonify(teacher)
    except psycopg2.Error as e:
        return jsonify(errorcodes.lookup(e.pgcode)), 409
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500
