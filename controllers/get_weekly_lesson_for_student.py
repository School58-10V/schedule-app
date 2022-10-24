import logging
from datetime import datetime
from typing import List
from urllib import request


from data_model.group import Group
from data_model.lesson_row import LessonRow
from data_model.location import Location
from data_model.student import Student
from data_model.students_for_groups import StudentsForGroups
from data_model.subject import Subject
from data_model.timetable import TimeTable
from data_model.user import User
from schedule_app import app
import jwt
from flask import request, jsonify

PUBLIC_KEY = open('./keys/schedule-public.pem').read()


def lesson_row_to_string(lesson_row: LessonRow) -> str:
    subject = Subject.get_by_id(lesson_row.get_subject_id(),
                                db_source=app.config.get('schedule_db_source')).get_subject_name()
    room = Location.get_by_id(lesson_row.get_room_id(),
                              db_source=app.config.get('schedule_db_source')).get_num_of_class()
    group = Group.get_by_id(lesson_row.get_group_id(), db_source=app.config.get('schedule_db_source'))
    group = str(group.get_grade()) + ' ' + group.get_letter()

    start_time = f'{lesson_row.get_start_time() // 100}:{lesson_row.get_start_time() % 100}' \
                 f'{"0" if lesson_row.get_start_time() % 100 == 0 else ""} '
    end_time = f'{lesson_row.get_end_time() // 100}:{lesson_row.get_end_time() % 100}{"0" if lesson_row.get_end_time() % 100 == 0 else ""}'

    lesson_row_to_string = f'{subject.capitalize()} с {start_time} до {end_time} в каб. ' \
                           f'{room}\nс классом/группой {group}'
    return lesson_row_to_string


@app.route("/api/v1/get-weekly-timetable-for-student/<name>", methods=["GET"])
def get_weekly_timetable(name):
    try:
        student_name = name
        student = Student.get_by_name(name=student_name, source=app.config.get('schedule_db_source'))
        student_id = student[0].get_main_id()
        student_groups = StudentsForGroups.get_group_by_student_id(student_id=student_id,
                                                                   db_source=app.config.get('schedule_db_source'))
        lesson_rows_list: List[LessonRow] = []
        year = datetime.now().year
        current_timetable = TimeTable.get_by_year(year, db_source=app.config.get('schedule_db_source'))
        tt = []
        for day in tt:
            for i in student_groups:
                var = [j for j in i.get_lesson_rows() if
                       j.get_day_of_the_week() == day and j.get_timetable_id() == current_timetable.get_main_id()]
                if var:
                    for j in var:
                        lesson_rows_list.append(j)
            tt[day] = lesson_rows_list
            lesson_rows_list = []

        for day in tt:
            day.sort(key=lambda x: x.get_start_time())
            tt[day] = day

        return jsonify(tt)
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500
