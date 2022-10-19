import jwt
import tabulate
from flask import request, jsonify

from data_model.lesson_row import LessonRow
from data_model.location import Location
from data_model.student import Student
from data_model.subject import Subject
from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from data_model.user import User
from schedule_app import app

PUBLIC_KEY = open('./keys/schedule-public.pem').read()


@app.route("/api/v1/week", methods=["GET"])
def get_week_schedule():

    try:
        request_token = request.headers.get('Authorization')
        data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
    except KeyError:
        return 'Не передан токен', 401

    user = User.get_by_login(login=data['login'], db_source=app.config.get('auth_db_source'))
    student_list = Student.get_by_name(name=user.get_name(), source=app.config.get('schedule_db_source'))

    if len(student_list) == 0:
        return 'Такого ученика не существует', 404
    if len(student_list) > 1:
        raise NotImplementedError('Если больше одного ученика с одним именем, мы падаем :(')

    lessonrow_list = LessonRow.get_all_by_student_id(student_list[0].get_main_id(),
                                                     db_source=app.config.get('schedule_db_source'))
    data = []
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', "Пятница", "Суббота", "Воскресенье"]
    for lr in lessonrow_list:
        obj = {
            'weekday': lr.get_day_of_the_week(),
            'subject': Subject.get_by_id(lr.get_subject_id(), db_source=app.config.get('schedule_db_source')).get_subject_name(),
            'start_time': LessonRow.prettify_time(lr.get_start_time()),
            'end_time': LessonRow.prettify_time(lr.get_end_time()),
            'location_number': Location.get_by_id(lr.get_room_id(), db_source=app.config.get('schedule_db_source')).get_num_of_class(),
            'teacher_full_name_list': [
                i.get_fio()
                for i in TeachersForLessonRows.get_teachers_by_lesson_row_id(
                    lr.get_main_id(), db_source=app.config.get('schedule_db_source'))
            ]
        }
        data.append(obj)
    data.sort(key=lambda x: weekdays.index(x['День недели']))

    pretty_data = tabulate.tabulate(data, headers='keys', tablefmt='grid')

    return pretty_data, 200
