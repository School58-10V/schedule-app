import jwt
from flask import request, jsonify
from tabulate import tabulate

from data_model.no_learning_period import NoLearningPeriod
from data_model.student import Student
from data_model.timetable import TimeTable
from data_model.user import User
from schedule_app import app

PUBLIC_KEY = open('./keys/schedule-public.pem').read()


@app.route('/api/v1/holidays/<int:year>', methods=['GET'])
def get_holidays_by_year(year: int):
    request_token = request.headers.get('Authorization')
    data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
    login = data['login']
    try:
        user = User.get_by_login(login, db_source=app.config.get('auth_db_source'))
        ##### Нужно ли проверять пароль? Если да, то как его передавать, через headers?
        name = user.get_name()

        student = Student.get_by_name(name=name, db_source=app.config.get('auth_db_source'))

    except ValueError:
        return '', 401

    try:
        timetable_id = TimeTable.get_by_year(year=year, db_source=app.config.get('auth_db_source')).get_main_id()
        nlp = NoLearningPeriod.get_all_by_timetable_id(timetable_id=timetable_id,
                                                       db_source=app.config.get('auth_db_source'))
        result = [(i.get_start_time(), i.get_end_time()) for i in nlp]
    except ValueError:
        return 'Нет расписания на этот год', 404
    return tabulate(sorted(result), ['Начало каникул', 'Конец каникул'], tablefmt='grid'), 200
