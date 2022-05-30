from __future__ import annotations
from typing import TYPE_CHECKING

import logging, psycopg2
from flask import request, jsonify

from data_model.teacher import Teacher
from data_model.lesson_row import LessonRow
from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from validators.lesson_row_validator import LessonRowValidator

from schedule_app import app

if TYPE_CHECKING:
    from flask import Response
    from typing import Union, Tuple


validator = LessonRowValidator()


@app.route("/api/v1/lesson-row", methods=["GET"])
def get_all_lesson_rows() -> Response | tuple[str, int]:
    """
    Достаем все LessonRow
    :return: Response
    """
    global_dct = []
    try:
        for i in LessonRow.get_all(app.config.get("schedule_db_source")):
            local_dct = i.__dict__()
            local_dct['teachers'] = [i.get_main_id() for i in TeachersForLessonRows.
                get_teachers_by_lesson_row_id(i.get_main_id(), db_source=app.config.get("schedule_db_source"))]
            global_dct.append(local_dct.copy())

        return jsonify(global_dct)
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route('/api/v1/lesson-row/detailed', methods=["GET"])
def get_all_lesson_row_detailed() -> Response:
    """
    Достаем все LessonRow вместе с учителями
    :return: Response
    """
    global_dct = []
    try:
        for i in LessonRow.get_all(app.config.get("schedule_db_source")):
            local_dct = i.__dict__()
            local_dct['teachers'] = [i.__dict__() for i in
                                    TeachersForLessonRows.get_teachers_by_lesson_row_id(
                                        i.get_main_id(),
                                        db_source=app.config.get("schedule_db_source"))]
            global_dct.append(local_dct.copy())
        return jsonify(global_dct)
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/lesson-row/<int:object_id>", methods=["GET"])
def get_lesson_row_by_id(object_id: int) -> Union[Response, Tuple[str, int]]:
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


@app.route('/api/v1/lesson-row/detailed/<int:object_id>', methods=['GET'])
def get_detailed_lesson_row_by_id(object_id: int) -> Union[Response, Tuple[str, int]]:
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
def create_lesson_row() -> Union[Response, Tuple[str, int]]:
    """
    Создаем LessonRow
    :return: Response
    """
    dct = request.get_json()
    try:
        validator.validate(dct, "POST")
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 400
    try:
        teacher_id = []
        if 'teachers' in dct:
            teacher_id = dct.pop('teachers')
        lesson_row = LessonRow(**dct, db_source=app.config.get("schedule_db_source")).save()
        for i in teacher_id:
            teacher = Teacher.get_by_id(i, db_source=app.config.get('schedule_db_source'))
            lesson_row.append_teacher(teacher)
        dct = lesson_row.__dict__()
        dct["object_id"] = lesson_row.get_main_id()
        dct['teachers'] = teacher_id
        return jsonify(dct)
    except (TypeError, ValueError):
        return '', 400
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/lesson-row/<int:object_id>", methods=["PUT"])
def update_lesson_rows(object_id: int) -> Union[Response, Tuple[str, int]]:
    """
    Обновляем LessonRow по данному id
    :param object_id:
    :return: Response
    """
    if request.get_json().get('object_id') != object_id:
        return "", 400

    dct = request.get_json()

    try:
        validator.validate(dct, method="PUT")
    except ValueError:
        return "", 400

    try:
        LessonRow.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404

    new_teachers_id = []
    try:
        if 'teachers' in dct:
            new_teachers_id = dct.pop('teachers')

        lesson_row_by_id = LessonRow(**dct, db_source=app.config.get('schedule_db_source')).save()
        old_teachers_id = [i.get_main_id() for i in lesson_row_by_id.get_teachers()]
        teachers_to_create = list((set(new_teachers_id) - set(old_teachers_id)))
        teachers_to_delete = list((set(old_teachers_id) - set(new_teachers_id)))

        try:
            for i in teachers_to_delete:
                teacher = Teacher.get_by_id(i, db_source=app.config.get('schedule_db_source'))
                lesson_row_by_id.remove_teacher(teacher)

            for i in teachers_to_create:
                teacher = Teacher.get_by_id(i, db_source=app.config.get('schedule_db_source'))
                lesson_row_by_id.append_teacher(teacher)

        except ValueError:
            return '', 400
        dct = lesson_row_by_id.__dict__()
        dct['teachers'] = new_teachers_id
        return jsonify(dct)
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/lesson-row/<int:object_id>", methods=["DELETE"])
def delete_lesson_row(object_id: int) -> Union[Response, Tuple[str, int]]:
    """
    Удаляем LessonRow по данному id
    :param object_id: int
    :return: Response
    """
    try:
        lesson_row = LessonRow.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        lesson_row = lesson_row.delete().__dict__()
    except psycopg2.Error as e:
        print(e)
        return jsonify(psycopg2.errorcodes.lookup(e.pgcode), 409)
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500
    return jsonify(lesson_row)
