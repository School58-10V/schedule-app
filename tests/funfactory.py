from __future__ import annotations
from typing import TYPE_CHECKING

import logging
from flask import jsonify

from data_model.group import Group
from data_model.lesson_row import LessonRow
from data_model.location import Location
from data_model.student import Student
from data_model.subject import Subject
from data_model.teacher import Teacher
import random
from schedule_app import app


class Funfactory:
    def __init__(self):
        self.__students_id = [79, 80, 123]
        self.__group_id = []

    @app.route("/api/v1/hinkali_makegroup", methods=["POST"])
    def create_fungroup():
        dct = {
            "class_letter": "В",
            "grade": 11,
            "profile_name": "Хинкали",
            "students": [79, 80, 123],
            "teacher_id": random.choice(Teacher.get_all(db_source=app.config.get("schedule_db_source"))).get_main_id()
        }
        try:
            student = []
            if 'students' in dct:
                student = dct.pop('students')
            group = Group(**dct, db_source=app.config.get("schedule_db_source")) \
                .save()
            for i in student:
                student1 = Student.get_by_id(i, db_source=app.config.get('schedule_db_source'))
                group.append_student(student1)
            dct = group.__dict__()
            dct['students'] = student
            return jsonify(dct)
        except Exception as err:
            logging.error(err, exc_info=True)
            return "", 500

    @app.route("/api/v1/hinkali_makelessonrow", methods=["POST"])
    def create_funlesson_row():
        dct = {
            "day_of_the_week": random.choice([0, 1, 2, 3, 4, 5, 6]),
            "end_time": 1130,
            "group_id": 54,
            "room_id": random.choice(Location.get_all(db_source=app.config.get("schedule_db_source"))).get_main_id(),
            "start_time": 1000,
            "subject_id": random.choice(Subject.get_all(db_source=app.config.get("schedule_db_source"))).get_main_id(),
            "teachers": [random.choice(Teacher.get_all(db_source=app.config.get("schedule_db_source"))).get_main_id()],
            "timetable_id": 1
        }
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
        except Exception as err:
            logging.error(err, exc_info=True)
            return "", 500

