import datetime
from schedule_app import app

from tabulate import tabulate

from data_model.lesson import Lesson
from data_model.lesson_row import LessonRow
from data_model.location import Location
from data_model.student import Student
from data_model.subject import Subject
from data_model.timetable import TimeTable
from interfaces.student_interface import StudentInterface


WEEKDAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']


def get_schedule_for_day(db_source, current_user_id, week_day):
    # Узнаем, какой год нам надо смореть
    timetable_id = TimeTable.get_by_year(datetime.date.today().year, db_source).get_main_id()
    # Берем все уроки, которые проходят сегодня
    lesson_rows = LessonRow.get_all_by_day(week_day=week_day,
                                           db_source=db_source)
    # Берем все замены, которые есть на сегодня
    lesson = {i.get_start_time(): i for i in Lesson.get_today_replacements(date=datetime.date.today(),
                                                                           db_source=db_source)}
    # Смотрим группы, которые есть у ученика
    groups_id = [i.get_main_id() for i in Student.get_by_id(current_user_id,
                                                            db_source).get_all_groups()]
    lesson_rows_dct = []
    for i in lesson_rows:
        # Если уроки проходят в этом году и у групп, в которые входить пользователь
        if i.get_timetable_id() == timetable_id and i.get_group_id() in groups_id:
            # То смотрим, есть ли на это время замена
            if i.get_start_time() not in lesson or \
                    lesson[i.get_start_time()].get_group_id() not in groups_id:
                # Если нету, то добавляем этот урок
                lesson_rows_dct.append(i)
            else:
                # Если есть, то добавляем вместо этого урока замену
                lesson_rows_dct.append(lesson[i.get_start_time()])
    # Сортируем то расписание, которое у нас получилось по началу урока
    lesson_rows_dct.sort(key=lambda x: x.get_start_time())
    # Возвращаем красивую табличку, где первый столбец - начало урока,
    # второй столбец - конец, третий - название урока, которое берем из subjecta
    data = [(i.get_start_time(), i.get_end_time(),
             Subject.get_by_id(i.get_subject_id(),
                               db_source).get_subject_name(),
             Location.get_by_id(i.get_room_id(), db_source).get_num_of_class())
            for i in lesson_rows_dct]
    nov_tb = [["", "Урока нет", ""] for i in range(9)]

    p = -1
    for i in nov_tb:
        p += 1
        if p == 0:
            i[0] = "Время"
            i[1] = datetime.date.today()
            i[2] = "КАБ."
        else:
            if p + 1 > 9:
                break
            if p > len(data):
                break
            i[0] = str(data[p - 1][0])[:-2] + ":" + str(data[p - 1][0])[2:] + "-" + str(data[p - 1][1] // 100) + ":" + str(data[p - 1][1] % 100)
            i[1] = data[p - 1][2]
            i[2] = data[p - 1][3]
    print(nov_tb)
    return nov_tb


def tmp(day):
    interface = StudentInterface(db_source=app.config.get('schedule_db_source'), student_id=80)
    return interface.get_schedule_for_day(day)


def schedule_for_week():
    interface = StudentInterface(db_source=app.config.get('schedule_db_source'), student_id=80)
    return '\n'.join(interface.get_schedule_for_week())