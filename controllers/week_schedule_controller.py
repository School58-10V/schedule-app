import jwt
import json
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
def get_schedule():
    weekday = json.loads(request.args.get('data'))

    try:
        request_token = request.headers.get('Authorization')
        data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
    except KeyError:
        return 'Не передан токен', 401

    user = User.get_by_login(login=data['login'], db_source=app.config.get('auth_db_source'))
    student = Student.get_by_id(element_id=80, db_source=app.config.get('schedule_db_source'))

    lessonrow_list = LessonRow.get_all_by_day(week_day=weekday,
                                                     db_source=app.config.get('schedule_db_source'))
    groups_id = [i.get_main_id() for i in Student.get_by_id(student.get_main_id(),
                                                db_source=app.config.get('schedule_db_source')).get_all_groups()]
    data = {
        'time': [],
        'name': [],
        'location': []
    }

    for lr in lessonrow_list:
        if lr.get_group_id() in groups_id:
            time = f'{LessonRow.prettify_time(lr.get_start_time())}:{LessonRow.prettify_time(lr.get_end_time())}'
            name = Subject.get_by_id(lr.get_subject_id(), db_source=app.config.get('schedule_db_source')).get_subject_name()
            location = Location.get_by_id(lr.get_room_id(), db_source=app.config.get('schedule_db_source')).get_num_of_class()

            data['time'].append(time)
            data['name'].append(name)
            data['location'].append(location)

    return data
