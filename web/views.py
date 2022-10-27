import datetime

from flask import render_template

from adapters.db_source import DBSource
from schedule_app import app

DBSOURCE = DBSource(host="postgresql.aakapustin.ru",
                    password="VYRL!9XEB3yXQs4aPz_Q",
                    user="schedule_app",
                    options="-c search_path=dbo,public")

BASE_PATH = '127.0.0.1:5000/api/v1'


@app.route('/', methods=['GET'])
def main_page():
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', "Пятница", "Суббота", "Воскресенье"]
    weekday_string = weekdays[datetime.date.today().weekday()]
    return render_template('main.html', weekday_string=weekday_string)


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
    context = {
        "object_type": "group",
        "inputs": [
            {"name": "grade", "label": "Класс", "type": "number"},
            {"name": "class_letter", "label": "Буква", "type": "text"},
            {"name": "profile_name", "label": "Профиль", "type": "text"},
            {"name": "students", "label": "ИД учеников", "type": "list"},
            {"name": "teacher_id", "label": "ИД Учителя", "type": "number"}
        ]
    }
    return render_template('groups.html', **context)


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
