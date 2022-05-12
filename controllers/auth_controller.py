import datetime

import jwt
from flask import Flask, request, jsonify
from jwt import DecodeError, ExpiredSignatureError

from services.db_source_factory import DBFactory

app = Flask(__name__)
dbf = DBFactory()

PRIVATE_KEY = open('schedule-key.pem').read()
PUBLIC_KEY = open('schedule-public.pem').read()

USERNAME, PASSWORD = 'test_user', 'test_password'

# устаревает через 2 недели
TOKEN_EXP_TIME = datetime.timedelta(days=14)


# Генерирует токен по информации о пользователе и возвращает его
@app.route('/login', methods=['POST'])
def login():
    username, password = request.json.get('username'), request.json.get('password')
    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    data = {
        'username': username, 'user_ip': user_ip,
        'user_agent': user_agent, "exp": datetime.datetime.now(tz=datetime.timezone.utc) + TOKEN_EXP_TIME
    }
    if not (username == USERNAME and password == PASSWORD):
        return jsonify(""), 401

    encoded_data = jwt.encode(data, PRIVATE_KEY, algorithm='RS256')
    return jsonify({'token': encoded_data})


@app.route('/test', methods=['POST', 'GET'])
def test():
    return jsonify({'yay': True}), 200


# Вызывается при каждом реквесте (кроме реквеста к /login)
# проверяет совпадение информации о пользователе с информацией из токена
# выбрасывает ошибку 400 когда токен некорректен
# выбрасывает ошибку 401 когда данные не соответствуют
@app.before_request
def before_request():
    # все get реквесты и /login реквесты пропускаем, авторизация не нужна
    if request.url_rule.rule == '/login' or request.method.lower() == 'get':
        return
    request_token = request.headers.get('Authorization')
    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    try:
        data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
    except DecodeError:
        return '', 400
    except ExpiredSignatureError:
        # ошибка:
        return '', 401
    if not (data.get('user_ip') == user_ip and data.get('user_agent') == user_agent):
        return '', 401


if __name__ == '__main__':
    app.run()
