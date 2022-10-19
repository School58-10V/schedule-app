from flask import request, render_template, session, redirect, url_for

from adapters.db_source import DBSource
from schedule_app import app

from interfaces.student_interface import StudentInterface
from interfaces.schedule_interface import get_schedule_for_today

DBSOURCE = DBSource(host="postgresql.aakapustin.ru",
                    password="VYRL!9XEB3yXQs4aPz_Q",
                    user="schedule_app",
                    options="-c search_path=dbo,public")

BASE_PATH = '127.0.0.1:5000/api/v1'


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main.html', schedule=get_schedule_for_today(db_source=DBSOURCE, current_user_id=119))


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout_page():
    return render_template('logout.html')


@app.route('/my-lessons', methods=['GET'])
def personal_lessons():
    return render_template('my_lessons.html')


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


@app.route('/timetable', methods=['GET'])
def timetable_page():
    return render_template('timetable.html')
