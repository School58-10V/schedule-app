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

        return jsonify(list(global_dct.values()))
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

@app.route("/api/v1/lesson-row/personal", methods=["GET"])
def get_lesson_row_by_day_and_student() -> Union[Response, Tuple[str, int]]:
    """
    Достаёт LessonRow по дню и айди студака
    :return: Response
    """
    try:
        # logging.debug("hi")
        day = request.args.get("day", None)
        student_id = request.args.get("student_id", None)
        # logging.debug(day + " ; " + student_id)
        if (day != None and student_id != None):
            rows = []
            data = LessonRow.get_by_day_and_student(int(day), int(student_id), app.config.get("schedule_db_source"))
            for row in data:
                local_dct = row.__dict__().copy()
                local_dct["subject_name"] = Subject.get_by_id(row.get_subject_id(), app.config.get("schedule_db_source")).get_subject_name()
                rows.append(local_dct)
            return jsonify(rows)
        else:
            return "", 400
    except Exception as e:
        print(e)
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

    validation_data = validator.validate(dct, method="PUT")
    if not validation_data[0]:
        return validation_data[1], 400

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
            # raw_row["start_time"] = prettify_time(row.get_start_time())
            raw_row["start_time"] = get_time_since_noon(prettify_time(row.get_start_time()))
            raw_row["end_time"] = get_time_since_noon(prettify_time(row.get_end_time()))
            raw_row["room"] = Location.get_by_id(row.get_room_id(), db_source).get_num_of_class()
            raw_row["group"] = Group.get_by_id(row.get_group_id(), db_source).__dict__()
            raw_row["subject"] = Subject.get_by_id(row.get_subject_id(), db_source).__dict__()
            result.append(raw_row.copy())
        return jsonify(result)
    except Exception as e:
        logging.error(e, exc_info=True)
        return "", 500


def prettify_time(time):
    """ Превращает тысяча десять в 10:10 """
    hours = time // 100
    minutes = time % 100
    return str(hours).zfill(2) + ':' + str(minutes).zfill(2)

def get_time_since_noon(time):
    hours = time.split(":")[0]
    minutes = time.split(":")[1]
    return minutes * 60000 + hours * 60 * 60000