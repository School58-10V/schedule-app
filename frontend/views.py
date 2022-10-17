import datetime

from flask import render_template
from tabulate import tabulate

from schedule_app import app
from interfaces.schedule_interface import get_schedule_for_today, get_schedule_for_week, get_schedule_for_day
from controllers.group_controller import get_groups
from controllers.lesson_controller import get_lessons
from controllers.student_controller import get_students
from controllers.subject_controller import get_subjects
from controllers.teacher_controller import get_teachers

BASE_PATH = '127.0.0.1:5000/api/v1'


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main.html',
                           schedule=tabulate(get_schedule_for_day(day=datetime.date.today().weekday(),
                                                                  user_id=124,
                                                                  db_source=app.config.get('schedule_db_source')),
                                             ["Предмет", "Время начала", "Место проведения"],
                                             tablefmt="grid"))


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
    # print(get_students().json)
    return render_template('students.html', students=get_students().json)


@app.route('/groups', methods=['GET'])
def groups_page():
    # print(list(get_groups()), dict(get_groups()), get_groups())

    return render_template('groups.html', groups=get_groups().json)


@app.route('/lessons', methods=['GET'])
def lessons_page():
    return render_template('lessons.html', lessons=get_lessons().json)


@app.route('/teachers', methods=['GET'])
def teachers_page():
    return render_template('teachers.html', teachers=get_teachers().json)


@app.route('/week-timetable', methods=['GET'])
def week_schedule_page():
    a = get_schedule_for_week(user_id=124, db_source=app.config.get('schedule_db_source'))
    return render_template('week_timetable.html',
                           schedule=a)


@app.route('/subjects', methods=['GET'])
def subjects_page():
    return render_template('subjects.html', subjects=get_subjects().json)


@app.route('/timetable', methods=['GET'])
def timetable_page():
    return render_template('timetable.html')
