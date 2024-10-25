import datetime

from tabulate import tabulate

from data_model.lesson import Lesson
from data_model.lesson_row import LessonRow
from data_model.location import Location
from data_model.student import Student
from data_model.subject import Subject
from data_model.timetable import TimeTable


def get_schedule_for_today(db_source, current_user_id):
    # Узнаем, какой год нам надо смореть
    timetable_id = TimeTable.get_by_year(datetime.date.today().year, db_source).get_main_id()
    # Берем все уроки, которые проходят сегодня
    lesson_rows = LessonRow.get_all_by_day(week_day=datetime.date.today().weekday(),
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
    if not data:
        return 'Сегодня уроков нет! Ура!'
    return f'Расписание на сегодня: {datetime.date.today()}\n' + \
           tabulate(data, ["Начало", "Конец", "Урок", "Кабинет"], tablefmt='grid')


def get_schedule_for_day(user_id, day, db_source):
    db_result = LessonRow.get_by_day_and_student(day, user_id, db_source)
    data = {"subj_names": [], "start_times": [], "locations": []}
    for lesson_row in db_result:
        data.get("subj_names").append(
            Subject.get_by_id(lesson_row.get_subject_id(), db_source=db_source).get_subject_name())
        data.get("start_times").append(lesson_row.get_start_time())
        location = Location.get_by_id(lesson_row.get_room_id(), db_source=db_source)
        if location.get_link() is None:
            data.get("locations").append(location.get_num_of_class())
        else:
            data.get("locations").append(location.get_link())
    return data


def get_schedule_for_week(db_source, user_id):
    week_dict = {0: "Понедельник",
                 1: "Вторник",
                 2: "Среда",
                 3: "Четверг",
                 4: "Пятница",
                 5: "Суббота",
                 6: "Воскресенье"}
    lst = []
    for i in range(0, 6):
        lst.append(f'{week_dict[i]}\n' + tabulate(get_schedule_for_day(day=i, db_source=db_source, user_id=user_id),
                                                  ["Предмет", "Время начала", "Место проведения"],
                                                  tablefmt="grid"))
    return lst
