import jwt, logging
from flask import request
from tabulate import tabulate

from data_model.no_learning_period import NoLearningPeriod
from data_model.student import Student
from data_model.teacher import Teacher
from data_model.timetable import TimeTable
from data_model.user import User
from schedule_app import app

PUBLIC_KEY = open('./keys/schedule-public.pem').read()
LOGGER = logging.getLogger("main.controller")


@app.route('/api/v1/holidays/<int:year>', methods=['GET'])
def get_holidays_by_year(year: int):
    request_token = request.headers.get('Authorization')
    data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
    login = data['login']
    try:
        name = User.get_by_login(login, db_source=app.config.get('auth_db_source')).get_name()
    except ValueError:
        LOGGER.error("Could not find the user while getting holidays by year!")
        return '', 401
        ##### Нужно ли проверять пароль? Если да, то как его передавать, через headers?

    student = Student.get_by_name(name=name, db_source=app.config.get('schedule_db_source'))
    teacher = Teacher.get_by_name(name=name, db_source=app.config.get('schedule_db_source'))
    if len(student + teacher) == 0:
        LOGGER.error("Could not find the user's student or teacher while getting holidays by year!")
        return '', 401

    try:
        timetable_id = TimeTable.get_by_year(year=year, db_source=app.config.get('schedule_db_source')).get_main_id()
        nlp = NoLearningPeriod.get_all_by_timetable_id(timetable_id=timetable_id,
                                                       db_source=app.config.get('schedule_db_source'))
        result = sorted([(nlp[i].get_start_time(),
                          nlp[i].get_stop_time())
                         for i in range(len(nlp))], key=lambda x: x[0])
        result = [(i + 1, result[i][0].strftime('%d-%m-%Y'),
                   result[i][1].strftime('%d-%m-%Y')) for i in range(len(result))]
    except (ValueError, IndexError):
        LOGGER.error("Could not find a timetable for this year!")
        return 'Нет расписания на этот год', 404
    return tabulate(result, ['№', 'Начало каникул', 'Конец каникул'], tablefmt='grid'), 200
