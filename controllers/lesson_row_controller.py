from __future__ import annotations
from typing import TYPE_CHECKING, Union
from validators.lesson_row_validator import LessonRowValidator
import psycopg2
from psycopg2 import errorcodes
from data_model.lesson_row import LessonRow
from flask import request, jsonify
from data_model.teachers_for_lesson_rows import TeachersForLessonRows


if TYPE_CHECKING:
    from flask import Response

from schedule_app import app

validator = LessonRowValidator()

@app.route("/api/v1/lesson-row", methods=["GET"])
def get_all_lesson_rows() -> Response:
    """
    Достаем все LessonRow
    :return: Response
    """
    global_dct = {'lesson_rows': []}
    for i in LessonRow.get_all(app.config.get("schedule_db_source")):
        local_dct = i.__dict__()
        local_dct['teachers'] = [i.get_main_id() for i in TeachersForLessonRows.
                                 get_teachers_by_lesson_row_id(i.get_main_id(), db_source=app.config.get("schedule_db_source"))]
        global_dct['lesson_rows'].append(local_dct.copy())

    return jsonify(global_dct)


@app.route('/api/v1/lesson-row/detailed', methods=["GET"])
def get_all_detailed() -> Response:
    """
    Достаем все LessonRow вместе с учителями
    :return: Response
    """
    global_dct = {'lesson_rows': []}
    for i in LessonRow.get_all(app.config.get("schedule_db_source")):
        local_dct = i.__dict__()
        local_dct['teachers'] = [i.__dict__() for i in TeachersForLessonRows.
            get_teachers_by_lesson_row_id(i.get_main_id(), db_source=app.config.get("schedule_db_source"))]
        global_dct['lesson_rows'].append(local_dct.copy())
    return jsonify(global_dct)


@app.route("/api/v1/lesson-row/<object_id>", methods=["GET"])
def get_lesson_row_by_id(object_id: int) -> Union[Response, tuple[str, int]]:
    """
    Достаем LessonRow по id
    :param object_id: int
    :return: Response
    """
    try:
        dct = LessonRow.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
        dct['teachers'] = [i.get_main_id() for i in TeachersForLessonRows.
            get_teachers_by_lesson_row_id(object_id, db_source=app.config.get("schedule_db_source"))]
        return jsonify(dct)
    except ValueError:
        return '', 404


@app.route('/api/v1/lesson-row/detailed/<object_id>', methods=['GET'])
def get_detailed_lesson_row_by_id(object_id: int) -> Union[Response, tuple[str, int]]:
    """
    Дастаем LessonRow по id вместе с учителями
    :param object_id: int
    :return: Response
    """
    try:
        dct = LessonRow.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
        dct['teachers'] = [i.__dict__() for i in TeachersForLessonRows.
            get_teachers_by_lesson_row_id(object_id, db_source=app.config.get("schedule_db_source"))]

        return jsonify(dct)
    except ValueError:
        return '', 404


@app.route("/api/v1/lesson-row", methods=["POST"])
def create_lesson_row() -> Union[Response, tuple[str, int]]:
    """
    Создаем LessonRow
    :return: Response
    """
    dct = request.get_json()
    try:
        validator.validate(dct, "POST")
    except:
        return '', 400
    try:
        teacher_id = []
        if 'teachers' in dct:
            teacher_id = dct.pop('teachers')
        lesson_row = LessonRow(**dct, db_source=app.config.get("schedule_db_source")).save()
        for i in teacher_id:
            TeachersForLessonRows(lesson_row_id=lesson_row.get_main_id(), teacher_id=i,
                                  db_source=app.config.get("schedule_db_source")).save()
        dct["object_id"] = lesson_row.get_main_id()
        dct['teachers'] = teacher_id
        return jsonify(dct)
    except TypeError:
        return '', 400
    except ValueError:
        return '', 401


@app.route("/api/v1/lesson-row/<object_id>", methods=["PUT"])
def update_lesson_rows(object_id: int) -> Union[Response, tuple[str, int]]:
    """
    Обновляем LessonRow по данному id
    :param object_id:
    :return: Response
    """
    dct = request.get_json()
    try:
        LessonRow.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        validator.validate(dct, method="PUT")
    except ValueError:
        return "", 400
    new_teachers_id = []
    if 'teachers' in dct:
        new_teachers_id = dct.pop('teachers')
    lesson_row_by_id = LessonRow.get_by_id(object_id, app.config.get("schedule_db_source"))
    lesson_row_by_id_dct = lesson_row_by_id.__dict__()
    lesson_row_by_id_dct['teachers'] = [i.get_main_id() for i in lesson_row_by_id.get_teachers()]
    old_teachers_id = lesson_row_by_id_dct.pop("teachers")
    teachers_to_create = list((set(new_teachers_id) - set(old_teachers_id)))
    teachers_to_delete = list((set(old_teachers_id) - set(new_teachers_id)))

    for i in range(len(teachers_to_delete)):
        tflr = TeachersForLessonRows.get_by_lesson_row_and_teacher_id(teacher_id=teachers_to_delete[i],
                                                                      lesson_row_id=object_id,
                                                                      db_source=app.config.get("schedule_db_source"))
        for j in tflr:
            j.delete()

    for i in teachers_to_create:
        TeachersForLessonRows(lesson_row_id=object_id, teacher_id=i,
                              db_source=app.config.get("schedule_db_source")).save()

    lesson_row = LessonRow(**dct, object_id=object_id, db_source=app.config.get("schedule_db_source")).save().__dict__()
    lesson_row['teachers'] = new_teachers_id
    return jsonify(lesson_row)


@app.route("/api/v1/lesson-row/<object_id>", methods=["DELETE"])
def delete_lesson_row(object_id: int) -> Union[Response, tuple[str, int]]:
    """
    Удаляем LessonRow по данному id
    :param object_id: int
    :return: Response
    """
    try:
        lesson_row = LessonRow.get_by_id(object_id, app.config.get("schedule_db_source"))
        lesson_row = lesson_row.delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        print(e)
        return jsonify(errorcodes.lookup(e.pgcode), 409)
    return jsonify(lesson_row)
