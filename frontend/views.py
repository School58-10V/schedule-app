from flask import request, render_template
from schedule_app import app


BASE_PATH = '127.0.0.1:5000/api/v1'


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main.html')


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')