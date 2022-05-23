from __future__ import annotations
from typing import Union, Any, TYPE_CHECKING, Tuple

import psycopg2

from data_model.lesson_row import LessonRow
from data_model.subject import Subject

if TYPE_CHECKING:
    from flask import Response

from data_model.teacher import Teacher
from data_model.teachers_for_subjects import TeachersForSubjects
from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from validators.teacher_validator import TeacherValidator
from flask import request, jsonify

from schedule_app import app

validator = TeacherValidator()


@app.route("/api/v1/teachers", methods=["GET"])
def get_teachers() -> Response:
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


@app.route("/api/v1/teachers/<int:object_id>", methods=["GET"])
def get_teacher_by_id(object_id: int) -> Union[Response, Tuple[str, int]]:
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
def get_detailed_teachers() -> Response:
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


@app.route("/api/v1/teachers/get/detailed/<int:object_id>", methods=["GET"])
def get_teacher_detailed_by_id(object_id: int) -> Union[Response, Tuple[str, int]]:
    try:
        teacher = Teacher.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
        teacher['subject_id'] = [i.__dict__() for i in TeachersForSubjects.
            get_subjects_by_teacher_id(object_id,
                                       db_source=app.config.get("schedule_db_source"))]
        teacher['lesson_row_id'] = [i.__dict__() for i in TeachersForLessonRows.
            get_lesson_rows_by_teacher_id(object_id,
                                          db_source=app.config.get("schedule_db_source"))]
        return jsonify(teacher)
    except ValueError:
        return '', 404


@app.route("/api/v1/teachers", methods=["POST"])
def create_teacher() -> Union[Tuple[str, int], Response]:
    dct = request.get_json()
    try:
        validator.validate(dct, "POST")
    except:
        return '', 400
    try:
        subject_id = []
        if 'subject_id' in dct:
            subject_id = dct.pop('subject_id')
        lesson_row_id = []
        if 'lesson_row_id' in dct:
            subject_id = dct.pop('lesson_row_id')

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

    except TypeError:
        return '', 400
    except ValueError as e:
        return '', 404


@app.route("/api/v1/teachers/<int:object_id>", methods=["PUT"])
def update_teacher(object_id: int) -> Union[Tuple[str, int], Response]:
    if request.get_json().get('object_id') != object_id:
        return "", 400
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    dct = request.get_json()
    try:
        Teacher.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    lesson_row_id = []
    if 'lesson_row_id' in dct:
        lesson_row_id += dct.pop('lesson_row_id')
    subject_id = []
    if 'subject_id' in dct:
        subject_id += dct.pop('subject_id')
    teacher = Teacher(**dct, db_source=app.config.get("schedule_db_source")).save()

    for i in teacher.get_lesson_rows():
        if i.get_main_id() not in lesson_row_id:
            teacher.remove_lesson_row(i)

    for i in teacher.get_subjects():
        if i.get_main_id() not in subject_id:
            teacher.remove_subject(i)

    try:
        for i in lesson_row_id:
            teacher.append_lesson_row(LessonRow.get_by_id(i, db_source=app.config.get("schedule_db_source")))

        for i in subject_id:
            teacher.append_subject(Subject.get_by_id(i, db_source=app.config.get("schedule_db_source")))
    except ValueError:
        return '', 400

    dct = teacher.__dict__()
    dct['subject_id'] = subject_id
    dct['lesson_row_id'] = lesson_row_id
    return jsonify(dct)


@app.route("/api/v1/teachers/<int:object_id>", methods=["DELETE"])
def delete_teacher(object_id: int) -> Union[Response, Tuple[str, int], Tuple[Any, int]]:
    try:
        return jsonify(Teacher.get_by_id(object_id, app.config.get("schedule_db_source")).delete().__dict__())
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400
