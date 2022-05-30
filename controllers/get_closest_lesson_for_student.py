import datetime
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
    subject = Subject.get_by_id(lesson_row.get_subject_id(), db_source=app.config.get('schedule_db_source')).get_subject_name()
    room = Location.get_by_id(lesson_row.get_room_id(), db_source=app.config.get('schedule_db_source')).get_num_of_class()
    group = Group.get_by_id(lesson_row.get_group_id(), db_source=app.config.get('schedule_db_source'))
    group = str(group.get_grade()) + ' ' + group.get_letter()

    # TODO: if time == 1103, str will be 11:3 instead of 11:03. fix later!
    start_time = f'{lesson_row.get_start_time() // 100}:{lesson_row.get_start_time() % 100}' \
                 f'{"0" if lesson_row.get_start_time() % 100 == 0 else ""} '
    end_time = f'{lesson_row.get_end_time() // 100}:{lesson_row.get_end_time() % 100}{"0" if lesson_row.get_end_time() % 100 == 0 else ""}'

    lesson_row_to_string = f'{subject.capitalize()} с {start_time} до {end_time} в каб. ' \
                           f'{room}\nс классом/группой {group}'
    return lesson_row_to_string


@app.route("/api/v1/get-closest-lesson-for-student", methods=["GET"])
def get_closest_lesson_for_student(current_datetime: datetime.datetime):
    request_token = request.headers.get('Authorization')
    data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
    login = data['login']
    student_name = User.get_by_login(login=login, db_source=app.config.get('auth_db_source')).get_name()
    student = Student.get_by_name(name=student_name, source=app.config.get('schedule_db_source'))

    student_id = student.get_main_id()
    student_groups = StudentsForGroups.get_group_by_student_id(student_id=student_id,
                                                               db_source=app.config.get('schedule_db_source'))
    lesson_rows_list: List[LessonRow] = []

    today = current_datetime.weekday()  # number 0-6
    current_timetable = TimeTable.get_by_year(db_source=app.config.get('auth_db_source'))

    for i in student_groups:
        var = [j for j in i.get_lesson_rows() if
               j.get_day_of_the_week() == today and j.get_timetable_id() == current_timetable.get_main_id()]
        if var:
            lesson_rows_list.append(*var)

    lesson_rows_list.sort(key=lambda x: x.get_start_time())
    if len(lesson_rows_list) == 0:
        return 'Сегодня уроков нет!'

    first_lesson_row = lesson_rows_list[0]

    weekday_to_text = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    return f'Ближайший урок сегодня, в {weekday_to_text[today]}: {lesson_row_to_string(first_lesson_row)}'


