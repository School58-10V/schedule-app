import jwt
from flask import Flask, request, jsonify
from jwt import DecodeError

from services.db_source_factory import DBFactory

app = Flask(__name__)
dbf = DBFactory()

PRIVATE_KEY = open('schedule-key.pem').read()
PUBLIC_KEY = open('schedule-public.pem').read()


# Генерирует токен по информации о пользователе и возвращает его
@app.route('/login', methods=['POST'])
def login():
    username, password = request.json.get('username'), request.json.get('password')
    if not authentication(username, password):
        return "", 401

    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    data = {'username': username, 'user_ip': user_ip, 'user_agent': user_agent}

    encoded_data = jwt.encode(data, PRIVATE_KEY, algorithm='RS256')
    return jsonify({'token': encoded_data})


@app.route('/test', methods=['POST'])
def test():
    return jsonify({'yay': True}), 200


# Вызывается при каждом реквесте (кроме реквеста к /login)
# Проверяет совпадение информации о пользователе с информацие из токена
# Выбрасывает ошибку 401 когда токен некорректен
# Выбрасывает ошибку 403 когда данные не соответствуют
@app.before_request
def before_request():
    if request.url_rule.rule == '/login' or request.method == "GET":
        return
    request_token = request.headers.get('Authorization')
    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    try:
        data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
    except DecodeError:
        return '', 401
    if not (data.get('user_ip') == user_ip and data.get('user_agent') == user_agent):
        return '', 403

def authentication(login, password):
    if login == "admin" and password == "password":
        return True
    return False

if __name__ == '__main__':
    app.run()
