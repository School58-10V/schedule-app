import json
import datetime
from flask import request, render_template

from adapters.db_source import DBSource
from schedule_app import app

from interfaces.student_interface import StudentInterface
from interfaces.schedule_interface import get_schedule_for_day, schedule_for_week

DBSOURCE = DBSource(host="postgresql.aakapustin.ru",
                    password="VYRL!9XEB3yXQs4aPz_Q",
                    user="schedule_app",
                    options="-c search_path=dbo,public")

BASE_PATH = '127.0.0.1:5000/api/v1'


@app.route('/', methods=['GET'])
def main_page():
    # st = StudentInterface(db_source=DBSOURCE, student_id=123)
    return render_template('main.html', schedule=get_schedule_for_day(db_source=DBSOURCE, current_user_id=80,
                                                                      week_day=datetime.date.today().weekday()))


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


@app.route('/add_teacher', methods=['GET'])
def teachers_addition_page():
    return render_template('add_teacher.html')


@app.route('/add_location', methods=['GET'])
def location_addition_page():
    return render_template('add_location.html')


@app.route('/add_group', methods=['GET'])
def group_addition_page():
    return render_template('add_group.html')


@app.route('/subjects', methods=['GET'])
def subjects_page():
    return render_template('subjects.html')


@app.route('/timetable', methods=['GET', 'POST'])
def timetable_page():
    return render_template('timetable.html')


@app.route('/timetable_week', methods=['GET'])
def timetable_week_page():
    schedule = schedule_for_week(db_source=DBSOURCE, current_user_id=80)
    return render_template('timetable_week.html', schedule=schedule)
    # return render_template('timetable_week.html', schedule=schedule_for_week(db_source=DBSOURCE, current_user_id=80,
    #                                                                            ))


@app.route('/timetable_for_week/<day>', methods=['GET', 'POST'])
def timetable_for_week_page(day):
    return render_template('timetable_for_week.html', schedule=get_schedule_for_day(db_source=DBSOURCE, current_user_id=80,
                                                                      week_day=day))
