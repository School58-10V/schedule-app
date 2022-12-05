import datetime

import jwt
import tabulate
from flask import request, jsonify

from data_model.lesson_row import LessonRow
from data_model.location import Location
from data_model.student import Student
from data_model.subject import Subject
from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from data_model.user import User
from interfaces.schedule_interface import get_schedule_for_day, get_schedule_for_week
from schedule_app import app

PUBLIC_KEY = open('./keys/schedule-public.pem').read()


@app.route("/api/v1/week", methods=["GET"])
def get_week_schedule1():
    request_token = request.headers.get('Authorization')
    data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
    user = User.get_by_login(data['login'], db_source=app.config.get('auth_db_source'))
    student_list = Student.get_by_name(name=user.get_name(), source=app.config.get('schedule_db_source'))

    if len(student_list) == 0:
        return 'Такого ученика не существует', 404
    if len(student_list) > 1:
        raise NotImplementedError('Если больше одного ученика с одним именем, мы падаем :(')
    res = get_schedule_for_week(user_id=student_list[0].get_main_id(),
                                db_source=app.config.get('schedule_db_source'))
    return jsonify(res)


@app.route("/api/v1/week1", methods=["GET"])
def get_week_schedule():
    # try:
    #     full_name = request.get_json()['full_name']
    # except KeyError as e:
        # TODO: поменять ид ошибки здесь
        # return 'Не указано имя ученика', 400

    request_token = request.headers.get('Authorization')
    data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
    user = User.get_by_login(data['login'], db_source=app.config.get('auth_db_source'))
    # user = User.get_by_login('mavovk', db_source=app.config.get('auth_db_source'))
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
            'День недели': weekdays[lr.get_day_of_the_week()],
            'Предмет': Subject.get_by_id(lr.get_subject_id(),
                                         db_source=app.config.get('schedule_db_source')).get_subject_name(),
            'Начальное время': LessonRow.prettify_time(lr.get_start_time()),
            'Конечное время': LessonRow.prettify_time(lr.get_end_time()),
            'Номер кабинета': Location.get_by_id(lr.get_room_id(),
                                                 db_source=app.config.get('schedule_db_source')).get_num_of_class(),
            'Учитель(ля)': ', '.join([
                i.get_fio()
                for i in TeachersForLessonRows.get_teachers_by_lesson_row_id(
                    lr.get_main_id(), db_source=app.config.get('schedule_db_source'))
                ])
            }
        data.append(obj)
    data.sort(key=lambda x: weekdays.index(x['День недели']))

    pretty_data = tabulate.tabulate(data, headers='keys', tablefmt='grid')

    return jsonify(pretty_data), 200

@app.route("/api/v1/week-raw/<int:student_id>", methods=["GET"])
def get_raw_week_schedule(student_id):

    # забираем все лессонроучики по данному расписанию для данного студа
    lesson_rows = LessonRow.get_all_by_student_id(student_id=student_id, db_source=app.config.get('schedule_db_source'))
    # Форматируем дату в норм табличку
    lesson_rows.sort(key= lambda x: x.get_start_time())
    data = {}
    for row in lesson_rows:
        subject = Subject.get_by_id(row.get_subject_id(), db_source=app.config.get('schedule_db_source'))
        lesson_data = {}
        lesson_data["object_id"] = row.get_main_id()
        lesson_data["subject"] = subject.get_subject_name()
        lesson_data["start"] = row.get_start_time()
        if (row.get_day_of_the_week() in data.keys()):
            data[row.get_day_of_the_week()].append(lesson_data)
        else:
            data[row.get_day_of_the_week()] = [lesson_data]
    return data, 200
