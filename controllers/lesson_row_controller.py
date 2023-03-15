from __future__ import annotations
from typing import TYPE_CHECKING

import logging, psycopg2
from flask import request, jsonify
from data_model.group import Group
from data_model.location import Location

from data_model.subject import Subject
from data_model.teacher import Teacher
from data_model.lesson_row import LessonRow
from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from validators.lesson_row_validator import LessonRowValidator
from services.logger.messages_templates import MessagesTemplates

from schedule_app import app
import time
from adapters.db_source import DBSource

if TYPE_CHECKING:
    from flask import Response
    from typing import Union, Tuple


validator = LessonRowValidator()


DAYS_OF_THE_WEEK = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье"
}

LOGGER = logging.getLogger("main.controller")
MESSAGES = MessagesTemplates()
MODEL = "LessonRow"


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
        LOGGER.info(MESSAGES.Controller.Success.get_collect_all_message(MODEL))
        return jsonify(global_dct)
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_collect_all(MODEL))
        LOGGER.exception(err)
        return "", 500


@app.route('/api/v1/lesson-row/detailed', methods=["GET"])
def get_all_lesson_row_detailed() -> Response:
    """
    Достаем все LessonRow вместе с учителями
    :return: Response
    """

    global_dct = {}
    try:
        columns = ['object_id', 'start_time', 'end_time', 'group_id', 'subject_id', 'room_id', 'timetable_id',
                   'day_of_the_week']

        result = LessonRow.get_detailed_lesson_rows()

        for el in result:
            lesson_row_info = dict(zip(columns, el[:-3]))

            if el[0] not in global_dct:
                lesson_row_info['teachers'] = []
            else:
                lesson_row_info = global_dct[el[0]]

            lesson_row_info['teachers'].append({'fio': el[-3], 'bio': el[-2], 'contacts': el[-1]})

            global_dct[el[0]] = lesson_row_info

        LOGGER.info(MESSAGES.Controller.Success.get_collect_all_detailed_message(MODEL))
        return jsonify(list(global_dct.values()))
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_collect_all_detailed_message(MODEL))
        LOGGER.exception(err)
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
        LOGGER.info(MESSAGES.Controller.Success.get_find_by_id_message(MODEL, object_id))
        return jsonify(dct)
    except ValueError as e:
        LOGGER.error(MESSAGES.Controller.Error.get_find_by_id_message(MODEL))
        LOGGER.exception(e)
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
        LOGGER.info(MESSAGES.Controller.Success.get_collect_all_detailed_message(MODEL))
        return jsonify(dct)
    except ValueError as e:
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
        LOGGER.exception(e)
        return '', 404

@app.route("/api/v1/lesson-row/personal", methods=["GET"])
def get_lesson_row_by_day_and_student() -> Union[Response, Tuple[str, int]]:
    """
    Достаёт LessonRow по дню и айди студака
    :return: Response
    """
    try:
        day = request.args.get("day", None)
        student_id = request.args.get("student_id", None)
        if (day != None and student_id != None):
            rows = []
            data = LessonRow.get_by_day_and_student(int(day), int(student_id), app.config.get("schedule_db_source"))
            for row in data:
                local_dct = row.__dict__().copy()
                local_dct["subject_name"] = Subject.get_by_id(row.get_subject_id(), app.config.get("schedule_db_source")).get_subject_name()
                rows.append(local_dct)
            LOGGER.info(MESSAGES.Controller.Success.get_find_by_day_and_student_message(MODEL))
            return jsonify(rows)
        else:
            LOGGER.error(MESSAGES.General.get_missing_fields_message("'day' and 'student_id'"))
            return "", 400
    except Exception as e:
        LOGGER.error(MESSAGES.Controller.Error.get_find_by_day_and_student_message(MODEL))
        return "", 404

@app.route("/api/v1/lesson-row", methods=["POST"])
def create_lesson_row() -> Union[Response, Tuple[str, int]]:
    """
    Создаем LessonRow
    :return: Response
    """
    dct = request.get_json()
    validation_data = validator.validate(dct, "POST")
    if not validation_data[0]:
        LOGGER.error(MESSAGES.General.get_validation_error_message(validation_data[1]))
        return validation_data[1], 400
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
        LOGGER.info(MESSAGES.Controller.Success.get_create_message(MODEL))
        return jsonify(dct)
    except (TypeError, ValueError) as err:
        LOGGER.error(MESSAGES.General.get_malformed_input_message())
        LOGGER.exception(err)
        return '', 400
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_create_message(MODEL))
        LOGGER.exception(err)
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

    validation_data = validator.validate(dct, method="PUT")
    if not validation_data[0]:
        LOGGER.error(MESSAGES.General.get_validation_error_message(validation_data[1]))
        return validation_data[1], 400

    try:
        LessonRow.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
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

        except ValueError as e:
            LOGGER.error(MESSAGES.Controller.Error.get_update_message(MODEL))
            LOGGER.exception(e)
            return '', 400
        dct = lesson_row_by_id.__dict__()
        dct['teachers'] = new_teachers_id
        LOGGER.info(MESSAGES.Controller.Success.get_update_message(MODEL))
        return jsonify(dct)
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_update_message(MODEL))
        LOGGER.exception(err)
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
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
        return "", 404
    try:
        lesson_row = lesson_row.delete().__dict__()
    except psycopg2.Error as e:
        LOGGER.error(MESSAGES.Controller.DBError.get_delete_message(MODEL, psycopg2.errorcodes.lookup(e.pgcode)))
        LOGGER.exception(e)
        return jsonify(psycopg2.errorcodes.lookup(e.pgcode), 409)
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_delete_message(MODEL))
        LOGGER.exception(err)
        return "", 500
    LOGGER.info(MESSAGES.Controller.Success.get_delete_message(MODEL))
    return jsonify(lesson_row)


@app.route("/api/v1/timetable/<int:timetable_id>/lesson-rows")
def get_lesson_row_by_timetable(timetable_id: int) -> Union[Tuple[str, int], Response]:
    db_source: DBSource = app.config.get("schedule_db_source")
    try:
        result = []
        for row in LessonRow.get_by_timetable_id(db_source, timetable_id):
            raw_row = row.__dict__()
            raw_row['teachers'] = [i.__dict__() for i in
                                        TeachersForLessonRows.get_teachers_by_lesson_row_id(
                                            row.get_main_id(),
                                            db_source=app.config.get("schedule_db_source"))]
            raw_row["start_time"] = prettify_time(row.get_start_time())
            raw_row["end_time"] = prettify_time(row.get_end_time())
            raw_row["day_of_the_week"] = DAYS_OF_THE_WEEK[row.get_day_of_the_week()]
            raw_row["room"] = Location.get_by_id(row.get_room_id(), db_source).get_num_of_class()
            raw_row["group"] = Group.get_by_id(row.get_group_id(), db_source).__dict__()
            raw_row["subject"] = Subject.get_by_id(row.get_subject_id(), db_source).__dict__()
            result.append(raw_row.copy())
        LOGGER.info(MESSAGES.Controller.Success.get_collect_all_by_model_message(MODEL, "Timetable"))
        return jsonify(result)
    except Exception as e:
        LOGGER.error(MESSAGES.Controller.Error.get_collect_all_by_model_message(MODEL, "Timetable"))
        LOGGER.exception(e)
        return "", 500


def prettify_time(time):
    """ Превращает тысяча десять в 10:10 """
    hours = time // 100
    minutes = time % 100
    return str(hours).zfill(2) + ':' + str(minutes).zfill(2)