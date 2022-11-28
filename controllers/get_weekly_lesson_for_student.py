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


@app.route("/api/v1/get-weekly-timetable-for-student", methods=["GET"])
def get_weekly_timetable():
    try:
        try:
            request_token = request.headers.get('Authorization')
            data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
        except KeyError:
            return 'Не передан токен', 401
        user = User.get_by_login(login=data['login'], db_source=app.config.get('auth_db_source'))

        student_name = user.get_name()
        student = Student.get_by_name(name=student_name, source=app.config.get('schedule_db_source'))
        student_id = student[0].get_main_id()
        student_groups = StudentsForGroups.get_group_by_student_id(student_id=student_id,
                                                                   db_source=app.config.get('schedule_db_source'))
        lesson_rows_list: List[LessonRow] = []
        year = datetime.now().year
        current_timetable = TimeTable.get_by_year(year, db_source=app.config.get('schedule_db_source'))
        tt = [0, 1, 2, 3, 4, 5, 6]
        for day in tt:
            for i in student_groups:
                var = [j for j in i.get_lesson_rows() if
                       j.get_day_of_the_week() == day and j.get_timetable_id() == current_timetable.get_main_id()]
                if var:
                    for j in var:
                        lesson_rows_list.append(j)

        lesson_rows_list.sort(key=lambda x: x.get_start_time())

        result = {'понедельник': [], 'вторник': [], 'среда': [], 'четверг': [],
                  'пятница': [], 'суббота': [], 'воскресенье': []}
        for i in lesson_rows_list:
            local_dict = i.__dict__()
            subject_name = Subject.get_by_id(local_dict["subject_id"], db_source=app.config.get('schedule_db_source'))\
                .get_subject_name()
            local_dict["subject_name"] = subject_name
            if i.get_day_of_the_week() == 0:
                result["понедельник"].append(local_dict)
            if i.get_day_of_the_week() == 1:
                result["вторник"].append(local_dict)
            if i.get_day_of_the_week() == 2:
                result['среда'].append(local_dict)
            if i.get_day_of_the_week() == 3:
                result['четверг'].append(local_dict)
            if i.get_day_of_the_week() == 4:
                result['пятница'].append(local_dict)
            if i.get_day_of_the_week() == 5:
                result['суббота'].append(local_dict)
            if i.get_day_of_the_week() == 6:
                result['воскресенье'].append(local_dict)

        return jsonify(result)
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500
