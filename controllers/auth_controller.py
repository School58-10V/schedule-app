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
    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    data = {'username': username, 'password': password, 'user_ip': user_ip, 'user_agent': user_agent}

    encoded_data = jwt.encode(data, PRIVATE_KEY, algorithm='RS256')
    return jsonify({'ok': True, 'token': encoded_data})


@app.route('/test', methods=['POST'])
def test():
    return jsonify({'yay': True}), 200


# Вызывается при каждом реквесте (кроме реквеста к /login)
# Проверяет совпадение информации о пользователе с информацие из токена
# Выбрасывает ошибку 400 когда токен некорректен
# Выбрасывает ошибку 401 когда данные не соответствуют
@app.before_request
def before_request():
    if request.url_rule.rule == '/login':
        return
    request_token = request.json.get('token')
    user_ip, user_agent = request.remote_addr, request.headers.get('user-agent')
    try:
        data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
    except DecodeError:
        return '', 400
    if not (data.get('user_ip') == user_ip and data.get('user_agent') == user_agent):
        return '', 401


if __name__ == '__main__':
    app.run()
