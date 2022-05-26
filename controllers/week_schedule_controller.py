import jwt
from flask import request, jsonify
from data_model.user import User
from data_model.student import Student

from schedule_app import app

PUBLIC_KEY = open('./keys/schedule-public.pem').read()


@app.route("/api/v1/week", methods=["GET"])
def get_week_schedule():
    request_token = request.headers.get('Authorization')
    data = jwt.decode(request_token, PUBLIC_KEY, algorithms=['RS256'])
    login = data['login']
    user = User.get_by_login(login=login, db_source=app.config.get('auth_db_source'))

    student = Student.get_by_name(name=user.get_name(), source=app.config.get('schedule_db_source'))
    print(user.get_name())

    return jsonify({})