from flask import request, render_template
from schedule_app import app


BASE_PATH = '127.0.0.1:5000/api/v1'


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main.html')


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout_page():
    return render_template('logout.html')


@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')


@app.route('/students', methods=['GET'])
def students_page():
    return render_template('students.html')


@app.route('/groups', methods=['GET'])
def groups_page():
    return render_template('groups.html')


@app.route('/lessons', methods=['GET'])
def lessons_page():
    return render_template('lessons.html')


@app.route('/teachers', methods=['GET'])
def teachers_page():
    return render_template('teachers.html')


@app.route('/subjects', methods=['GET'])
def subjects_page():
    return render_template('subjects.html')