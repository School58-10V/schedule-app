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
    # nov_tb = [["", "Урока нет", ""] for i in range(9)]
    nov_tb = [['Время', datetime.date.today().strftime("%d.%m.%Y"), 'Кабинет']]

    print(data)

    for el in data:
        nov_tb.append([
                f'{str(el[0])[:-2]}:{str(el[0])[2:]}-{str(el[1] // 100)}:{str(el[1] % 100)}',
                el[2],
                el[3]
            ])

    nov_tb += [["", "Урока нет", ""]] * (9 - len(data))

    return nov_tb


def schedule_for_week(db_source, current_user_id):
    week = []
    for i in range(8):
        # Узнаем, какой год нам надо смореть
        timetable_id = TimeTable.get_by_year(datetime.date.today().year, db_source).get_main_id()
        # Берем все уроки, которые проходят сегодня
        lesson_rows = LessonRow.get_all_by_day(week_day=i,
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
        data = [Subject.get_by_id(i.get_subject_id(), db_source).get_subject_name()
                for i in lesson_rows_dct]
        week.append(data)
    nov_tb = [["Урока нет" for i in range(8)] for i in range(6)]
    p = -1
    for ii in range(len(nov_tb)):
        p += 1
        c = -1
        for iii in range(len(nov_tb[ii])):
            c += 1
            if c > len(week[ii]) - 1 or len(week[ii]) == 0:
                break
            nov_tb[ii][iii] = week[ii][iii]
    return nov_tb
