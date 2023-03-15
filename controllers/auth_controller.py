from __future__ import annotations
from typing import TYPE_CHECKING

import datetime, jwt, logging
from flask import request, jsonify, g
from jwt import DecodeError, ExpiredSignatureError

from data_model.user import User
from services.logger.messages_templates import MessagesTemplates

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

LOGGER = logging.getLogger("main.controller")
MESSAGES = MessagesTemplates()


# Генерирует токен по информации о пользователе и возвращает его
@app.route('/api/v1/login', methods=['POST'])
def do_login() -> Union[Tuple[Response, int], Tuple[str, int], Response]:
    LOGGER.debug(MESSAGES.Authentication.get_login_attempt_message())

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
        LOGGER.warning(MESSAGES.Authentication.get_wrong_login_message(login))
        return 'Incorrect login', 401
    if not user.compare_hash(password):
        LOGGER.warning(MESSAGES.Authentication.get_wrong_password_message())
        return jsonify("Incorrect password"), 401
    encoded_data = jwt.encode(data, PRIVATE_KEY, algorithm='RS256')
    LOGGER.info(MESSAGES.Authentication.get_login_success_message())
    return jsonify({'token': encoded_data})


@app.route('/api/v1/register', methods=['POST'])
def register() -> Response:
    LOGGER.debug(MESSAGES.Authentication.get_register_attempt_message())

    login, fullname, password = request.json.get('login'), request.json.get('fullname'), request.json.get('password')
    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    data = {
        'login': login, 'user_ip': user_ip,
        'user_agent': user_agent, "exp": datetime.datetime.now(tz=datetime.timezone.utc) + TOKEN_EXP_TIME
        }
    encoded_data = jwt.encode(data, PRIVATE_KEY, algorithm='RS256')
    user = User(login=login, password=password, name=fullname, db_source=app.config.get('auth_db_source'))
    user.save()

    LOGGER.info(MESSAGES.Authentication.get_register_success_message())
    return jsonify({'token': encoded_data})


# Вызывается при каждом реквесте (кроме реквеста к /login)
# проверяет совпадение информации о пользователе с информацией из токена
# выбрасывает ошибку 400 когда токен некорректен
# выбрасывает ошибку 401 когда данные не соответствуют
@app.before_request
def before_request() -> Optional[Tuple[str, int]]:
    # все get реквесты и /login реквесты пропускаем, авторизация не нужна
    # TODO: добавить исключения для get метода(dict с включениями/исключениями методов)

    # # urls, где наличие токена ОБЯЗАТЕЛЬНО, * - все эндпоинты
    # included_urls = {
    #     'GET': ['/api/v1/profile'],
    #     'OPTIONS': [],
    #     'POST': []
    # }
    #
    # # urls, где наличие токена не требуется(меньше приоритет, чем у included)
    # excluded_urls = {
    #     'GET': [],
    #     'OPTIONS': ['*'],
    #     'POST': ['/api/v1/login', '/api/v1/register']
    # }

    LOGGER.info(MESSAGES.Authentication.get_on_request_message(request.method, request.path, request.host, request.host_url))

    if request.url_rule is None or \
            request.path == '/api/v1/login' or \
            request.path == '/api/v1/register' or \
            (request.method.lower() == 'get' and request.path != '/api/v1/profile') or\
            request.method.lower() in ['post', 'options']:
        return
    request_token = request.headers.get('Authorization')
    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    try:
        data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
        g.user = User.get_by_login(data['login'], db_source=app.config.get('auth_db_source'))
    except (DecodeError, ExpiredSignatureError):
        LOGGER.warning(MESSAGES.Authentication.get_malformed_request_message())
        return '', 400
    except AttributeError:
        LOGGER.warning(MESSAGES.Authentication.get_token_not_found_message())
        return 'No token', 400
    if not (data.get('user_ip') == user_ip and data.get('user_agent') == user_agent):
        LOGGER.warning(MESSAGES.Authentication.get_session_change_message())
        return '', 401
