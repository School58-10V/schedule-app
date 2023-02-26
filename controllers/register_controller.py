from __future__ import annotations
from typing import TYPE_CHECKING

import datetime, jwt
from flask import request, jsonify
from jwt import DecodeError, ExpiredSignatureError

from data_model.users_for_students import UsersForStudents
from data_model.teacher import Teacher
from data_model.users_for_teachers import UsersForTeachers
from data_model.user import User
from data_model.student import Student
from schedule_app import app

if TYPE_CHECKING:
    from flask import Response
    from typing import Tuple, Union, Optional

# TODO: тоже заимплементить конфиг (убрать точки со слешами)
PRIVATE_KEY = open('./keys/schedule-key.pem').read()
PUBLIC_KEY = open('./keys/schedule-public.pem').read()

# устаревает через 2 недели
# TODO: потом заимплементить вынос в конфиг
TOKEN_EXP_TIME = datetime.timedelta(days=14)


@app.route('/api/v1/register/teacher', methods=['POST'])
def register() -> Response:
    login, fullname, password = request.json.get('login'), request.json.get('fullname'), request.json.get('password')
    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    data = {
        'login': login, 'user_ip': user_ip,
        'user_agent': user_agent, "exp": datetime.datetime.now(tz=datetime.timezone.utc) + TOKEN_EXP_TIME
        }
    encoded_data = jwt.encode(data, PRIVATE_KEY, algorithm='RS256')
    user = User(status=1, login=login, password=password,
                name=fullname, db_source=app.config.get('auth_db_source')).save()
    add_student_to_user(user.get_main_id(), add_student(user.get_name()))
    return jsonify({'token': encoded_data})


@app.route('/api/v1/register/student', methods=['POST'])
def register() -> Response:
    login, fullname, password = request.json.get('login'), request.json.get('fullname'), request.json.get('password')
    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    data = {
        'login': login, 'user_ip': user_ip,
        'user_agent': user_agent, "exp": datetime.datetime.now(tz=datetime.timezone.utc) + TOKEN_EXP_TIME
        }
    encoded_data = jwt.encode(data, PRIVATE_KEY, algorithm='RS256')
    user = User(status=0, login=login, password=password,
                name=fullname, db_source=app.config.get('auth_db_source')).save()
    add_teacher_to_user(user.get_main_id(), add_teacher(user.get_name()))
    return jsonify({'token': encoded_data})


def add_teacher(name: str) -> int:
    if len(Teacher.get_by_name(name, db_source=app.config.get('schedule_db_source'))) == 0:
        Teacher(fio=name, db_source=app.config.get('schedule_db_source')).save()
    else:
        return 'Name is duplicated', 400
    return Teacher.get_by_name(name, db_source=app.config.get('schedule_db_source'))[0].get_main_id()


def add_student(name: str) -> int:
    if len(Student.get_by_name(name, source=app.config.get('schedule_db_source'))) == 0:
        Student(full_name=name, db_source=app.config.get('schedule_db_source')).save()
    else:
        return 'Name is duplicated', 400
    return Student.get_by_name(name, source=app.config.get('schedule_db_source'))[0].get_main_id()


def add_teacher_to_user(user_id: int, teacher_id: int) -> int:
    return UsersForTeachers(user_id=user_id, teacher_id=teacher_id,
                            db_source=app.config.get('schedule_db_source')).save().get_main_id()


def add_student_to_user(user_id: int, student_id: int) -> int:
    return UsersForStudents(user_id=user_id, student_id=student_id,
                            db_source=app.config.get('schedule_db_source')).save().get_main_id()
