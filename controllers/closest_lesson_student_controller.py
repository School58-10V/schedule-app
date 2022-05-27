import datetime
from typing import List

from flask import request, jsonify, Response

from data_model.lesson_row import LessonRow
from data_model.student import Student
from data_model.students_for_groups import StudentsForGroups
from data_model.timetable import TimeTable
from data_model.user import User
from schedule_app import app


@app.route("/api/v1/get-closest-lesson-for-student", methods=["GET"])
def get_closest_lesson_for_student(self, current_datetime: datetime.datetime):
    login, password = request.json.get('login'), request.json.get('password')
    try:
        user = User.get_by_login(login=login, db_source=app.config.get('auth_db_source'))
        full_name = user.get_name()
        student = Student.get_by_name(name=full_name, db_source=app.config.get('auth_db_source'))
    except ValueError:
        return '', 401
    student_groups = StudentsForGroups.get_group_by_student_id(student, self.__db_source)
    lesson_rows_list: List[LessonRow] = []

    today = current_datetime.weekday()  # number 0-6
    current_timetable = TimeTable.get_by_year(self.__db_source)

    for i in student_groups:
        # надо бы переписать
        # здесь добавляются лессон_ровс если они из этого года и этого дня недели
        var = [j for j in i.get_lesson_rows() if
                j.get_day_of_the_week() == today and j.get_timetable_id() == current_timetable.get_main_id()]
        if var:
            lesson_rows_list.append(*var)

    lesson_rows_list.sort(key=lambda x: x.get_start_time())
    if len(lesson_rows_list) == 0:
        return 'Сегодня уроков нет!'

    first_lesson_row = lesson_rows_list[0]

    weekday_to_text = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    return f'Ближайший урок сегодня, в {weekday_to_text[today]}: {self.__lesson_row_to_string(first_lesson_row)}'