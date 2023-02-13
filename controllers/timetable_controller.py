from __future__ import annotations

import io
from typing import TYPE_CHECKING

import psycopg2, logging
from flask import request, jsonify

from schedule_app import app

from data_model.lesson_row import LessonRow
from data_model.location import Location
from data_model.teacher import Teacher
from data_model.timetable import TimeTable
from data_model.group import Group
from data_model.subject import Subject

from validators.timetable_validator import TimetableValidator
from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from flask import Response
    from typing import Union, Any, Tuple

validator = TimetableValidator()

DAY_CODES = {
    '10000': 0,
    '01000': 1,
    '00100': 2,
    '00010': 3,
    '00001': 4
}
PERIOD_CODES = {
    1: (900, 945),
    2: (955, 1040),
    3: (1100, 1145),
    4: (1155, 1240),
    5: (1300, 1345),
    6: (1355, 1440),
    7: (1500, 1545),
    8: (1555, 1640),
}


def parse_file(file):
    return BeautifulSoup(file, 'html.parser', from_encoding='utf-8')


def get_information(tag, fields, xml_data):
    elements = {}
    if tag == 'period':
        for el in xml_data.findAll(tag):
            info = {}
            for field in fields:
                info[field] = el.get(field)
            elements[el.get('name')] = info
    elif tag == 'daysdef':
        for el in xml_data.findAll(tag):
            info = {}
            for field in fields:
                info[field] = el.get(field)

            elements[el.get('days')] = info
    else:

        for el in xml_data.findAll(tag):
            info = {'id': el.get('id')}
            for field in fields:
                info[field] = el.get(field)

            elements[info['id']] = info

    return elements


@app.route("/api/v1/timetable", methods=["GET"])
def get_timetable() -> Response:
    try:
        return jsonify([i.__dict__() for i in TimeTable.get_all(app.config.get("schedule_db_source"))])
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/timetable/<int:object_id>", methods=["GET"])
def get_timetable_by_id(object_id) -> Response:
    try:
        return jsonify(TimeTable.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
    except ValueError:
        return "", 404


@app.route("/api/v1/timetable", methods=["POST"])
def create_timetable() -> Union[Response, Tuple[str, int]]:
    try:
        validator.validate(request.get_json(), "POST")
    except ValueError:
        return "", 400
    try:
        return jsonify(TimeTable(**request.get_json(),
                                 db_source=app.config.get("schedule_db_source")).save().__dict__())
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/timetable/<int:object_id>", methods=["PUT"])
def update_timetable(object_id: int) -> Union[Tuple[str, int], Response]:
    if request.get_json().get('object_id') != object_id:
        return "", 400
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        TimeTable.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        return jsonify(TimeTable(**request.get_json(),
                                 db_source=app.config.get("schedule_db_source")).save().__dict__())
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/timetable/<int:object_id>", methods=["DELETE"])
def delete_timetable(object_id: int) -> Union[Response, Tuple[str, int], Tuple[Any, int]]:
    try:
        timetable = TimeTable.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        timetable = timetable.delete().__dict__()
        return jsonify(timetable)
    except psycopg2.Error as e:
        return jsonify(psycopg2.errorcodes.lookup(e.pgcode)), 409
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route('/api/v1/timetable/upload', methods=['POST'])
def upload_files():
    data = request.files['file']

    try:
        xml_data = parse_file(data.read())

        subjects = get_information('subject', ['name'], xml_data)
        teachers = get_information('teacher', ['name'], xml_data)
        classrooms = get_information('classroom', ['name'], xml_data)
        classes = get_information('class', ['name', 'teacherid'], xml_data)
        groups = get_information('group', ['name', 'classid'], xml_data)

        lessons_dict = {}

        for el in xml_data.findAll('lesson'):
            info = {}
            try:
                info['subject'] = subjects[el.get('subjectid')]
            except KeyError:
                info['subject'] = '---'

            try:
                info['teacher'] = teachers[el.get('teacherids')]
            except KeyError:
                info['teacher'] = '---'

            try:
                info['classroom'] = classrooms[el.get('classroomids')]
            except KeyError:
                info['classroom'] = '---'

            try:
                info['class'] = classes[el.get('classids')]['name']
            except KeyError:
                info['class'] = '---'

            try:
                info['group'] = groups[el.get('groupids')]['name']
            except KeyError:
                info['group'] = '---'

            lessons_dict[el.get('id')] = info

        cards = []
        for el in xml_data.findAll('card'):
            info = lessons_dict[el.get('lessonid')]
            info['day'] = el.get('days')
            info['period'] = int(el.get('period'))
            cards.append(info)

        timetable = {}

        for el in cards:
            if el['class'] not in timetable:
                timetable[el['class']] = {}
            if el['day'] not in timetable[el['class']]:
                timetable[el['class']][el['day']] = []

            timetable[el['class']][el['day']].append(el)

        for el in timetable.values():
            for day in el:
                el[day] = sorted(el[day], key=lambda x: x['period'])

        timetable['classes'] = [el['name'] for el in classes.values()]
        timetable['amount_of_days'] = len(xml_data.findAll('daysdef')) - 2

        return jsonify(timetable), 200
    except Exception as e:
        print(e)
        return '', 500


@app.route('/api/v1/timetable/save', methods=['POST'])
def save_timetable():
    data = request.get_json()

    for el in data['classes']:
        try:
            for day in data[el]:
                for lesson in data[el][day]:
                    add_lesson_row(lesson, day, lesson['period'])
        except KeyError:
            pass

    return '', 200


def parse_grade(name: str) -> tuple[int, str]:
    grade = ''
    letter = ''

    for el in name:
        if el.isdigit():
            grade += el
        else:
            letter += el

    return int(grade), letter


def add_location(information: dict) -> int:
    return Location(num_of_class=int(information['classroom']['name']), location_type='classroom',
                    db_source=app.config.get("schedule_db_source")).save().get_main_id()


def add_subject(information: dict) -> int:
    return Subject(subject_name=information['name'],
                   db_source=app.config.get("schedule_db_source")).save().get_main_id()


def add_teacher(information: dict) -> int:
    parameters = {
        'fio': information['teacher']['name']
    }

    try:
        office_id = Location.get_by_number(int(information['classroom']['name']),
                                           app.config.get("schedule_db_source")).get_main_id()
    except IndexError:
        office_id = add_location(information)

    information['office_id'] = office_id

    return Teacher(**parameters, db_source=app.config.get('schedule_db_source')).save().get_main_id()


def add_group(information: dict) -> int:
    parameters = {
        'class_letter': information['group'],
        'grade': information['class'],
    }

    try:
        teacher_id = Teacher.get_by_name(information['teacher']['name'],
                                         app.config.get("schedule_db_source"))[0].get_main_id()
    except IndexError:
        teacher_id = add_teacher(information)

    parameters['teacher_id'] = teacher_id

    return Group(**parameters, db_source=app.config.get('schedule_db_source')).save().get_main_id()


def add_lesson_row(lesson: dict, day: str, period: int) -> None:
    parameters = {
        'day_of_the_week': DAY_CODES[day],
        'start_time': PERIOD_CODES[period][0],
        'end_time': PERIOD_CODES[period][1],
        'timetable_id': 49
    }

    grade, letter = parse_grade(lesson['class'])
    lesson['group'] = f'{letter} {lesson["group"]}'
    lesson['class'] = grade

    try:
        group_id = Group.get_by_class_letters(app.config.get("schedule_db_source"), lesson['group'],
                                              lesson['class'])[0].get_main_id()
    except IndexError:
        group_id = add_group(lesson)

    try:
        subject_id = Subject.get_by_query({'subject_name': lesson['subject']['name']},
                                          app.config.get("schedule_db_source"))[0].get_main_id()
    except IndexError:
        subject_id = add_subject(lesson['subject'])

    try:
        room_id = Location.get_by_number(int(lesson['classroom']['name']),
                                         app.config.get("schedule_db_source")).get_main_id()
    except IndexError:
        room_id = add_location(lesson)

    parameters['group_id'] = group_id
    parameters['subject_id'] = subject_id
    parameters['room_id'] = room_id

    LessonRow(**parameters, db_source=app.config.get('schedule_db_source')).save()
