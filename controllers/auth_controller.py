from __future__ import annotations
from typing import TYPE_CHECKING

import datetime, jwt
from flask import request, jsonify
from jwt import DecodeError, ExpiredSignatureError

from data_model.user import User
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


# Генерирует токен по информации о пользователе и возвращает его
@app.route('/api/v1/login', methods=['POST'])
def do_login() -> Union[Tuple[Response, int], Tuple[str, int], Response]:
    login, password = request.json.get('login'), request.json.get('password')
    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    # TODO: if login/password are missing, abort
    data = {
        'login': login, 'user_ip': user_ip,
        'user_agent': user_agent, "exp": datetime.datetime.now(tz=datetime.timezone.utc) + TOKEN_EXP_TIME
        }
    try:
        user = User.get_by_login(login=login, db_source=app.config.get('auth_db_source'))
    except ValueError:
        return '', 401
    if not user.compare_hash(password):
        return jsonify(""), 401
    encoded_data = jwt.encode(data, PRIVATE_KEY, algorithm='RS256')
    return jsonify({'token': encoded_data})


@app.route('/api/v1/register', methods=['POST'])
def register() -> Response:
    login, fullname, password = request.json.get('login'), request.json.get('fullname'), request.json.get('password')
    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    data = {
        'login': login, 'user_ip': user_ip,
        'user_agent': user_agent, "exp": datetime.datetime.now(tz=datetime.timezone.utc) + TOKEN_EXP_TIME
        }
    encoded_data = jwt.encode(data, PRIVATE_KEY, algorithm='RS256')
    user = User(login=login, password=password, name=fullname, db_source=app.config.get('auth_db_source'))
    user.save()
    return jsonify({'token': encoded_data})


# Вызывается при каждом реквесте (кроме реквеста к /login)
# проверяет совпадение информации о пользователе с информацией из токена
# выбрасывает ошибку 400 когда токен некорректен
# выбрасывает ошибку 401 когда данные не соответствуют
@app.before_request
def before_request() -> Optional[Tuple[str, int]]:
    # все get реквесты и /login реквесты пропускаем, авторизация не нужна
    if request.url_rule is None or \
            request.path == '/api/v1/login' or \
            request.path == '/api/v1/register' or \
            request.method.lower() == 'get' or request.method.lower() == 'options':
        return
    request_token = request.headers.get('Authorization')
    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    try:
        data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
    except (DecodeError, ExpiredSignatureError):
        return '', 400
    if not (data.get('user_ip') == user_ip and data.get('user_agent') == user_agent):
        return '', 401

