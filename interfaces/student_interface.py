import datetime
from typing import List, Any

from tabulate import tabulate
from adapters.abstract_source import AbstractSource
from data_model.lesson import Lesson
from data_model.lesson_row import LessonRow
from data_model.location import Location
from data_model.student import Student
from data_model.subject import Subject
from data_model.teacher import Teacher
from data_model.timetable import TimeTable
from adapters.db_source import DBSource
from data_model.location import Location
from data_model.group import Group
from data_model.students_for_groups import StudentsForGroups
from data_model.teachers_for_lesson_rows import TeachersForLessonRows


class StudentInterface:

    def __init__(self, db_source: DBSource, student_id: int):
        self.__current_user_id = student_id
        self.__current_user = str(student_id)  # TODO: сделать это именем, т.е. получить имя студента через БД
        self.__db_source = db_source
        self.__log = False
        self.__today = datetime.date.today()
        self.__current_year = self.__today.year
        self.__current_day_of_week = self.__today.weekday()  # передается от 0 до 6, нужно обсудить в каком формате у нас день недели в итоге

        self.__login()

    def __login(self, initial: bool = True):
        username = self.__smart_input('Ваше ФИО: ')
        if self.__check_student_name(username):
            self.__current_user_id, self.__current_user = self.__get_current_user_info(username)
            print(f'Успешно зашли под именем {username}!')
            self.__log = True
            if initial:
                input()
                self.main_loop()
        else:
            print(f'Такого ученика не существует.')
            self.__login(initial)

    def __logout(self):
        self.__current_user = None
        self.__log = False
        print('Вы успешно вышли!')

    def main_loop(self):
        while self.__log:
            print()
            print(tabulate([(1, "Информация о учителе"),
                            (2, "Узнать классного руководителя ученика"),
                            (3, "Мое следующее занятие сегодня"),
                            (4, "Информация о каникулах"),
                            (5, "Информация о заменах"),
                            (6, "Расписание"),
                            (0, "Выйти из аккаунта")], ['Опция', 'Команда'], tablefmt='grid'))
            option = self.__smart_input(
                'Ваша опция (используйте "exit" или "выйти" чтобы в любой момент выйти в главное меню): '
            )
            if option == '1':
                self.__teacher_info()
            elif option == '2':
                self.__get_class_teacher()
            elif option == '3':
                self.__my_next_lesson()
            elif option == '4':
                self.__holidays()
            elif option == '5':
                self.__replacements()
            elif option == '6':
                self.__schedule()
            elif option == '0':
                self.__logout()
                self.__log = False
                self.__login(False)
            else:
                print('Неверная опция!')
            input()

    def __schedule(self):
        while True:
            option = int(self.__smart_input('Напишите 1 - чтобы посмотреть расписание на сегодня\n'
                                            'Напишите 2 - чтобы посмотреть расписание на неделю\n'
                                            'Напишите 3 - чтобы посмотреть расписание на какой-либо день\n'))
            if option in [1, 2, 3]:
                break
            else:
                print('Некорректное число')

        if option == 1:
            print(self.__get_schedule_for_today())
        elif option == 2:
            self.__get_schedule_for_week()
        elif option == 3:
            day = int(self.__smart_input('''
Напишите день на котороый хотите посмотреть расписание
Понедельник - 1
Вторник - 2
Среда - 3
Четверг - 4
Пятница - 5
 '''))
            print(tabulate(self.__get_schedule_for_day(day - 1), ["Предмет", "Время начала", "Место проведения"],
                           tablefmt="grid"))

    def __replacements(self):
        v_replacements = self.__smart_input(
            "Выбирите опцию:\n"
            "1. Мои замены на сегодняшний день\n"
            "2. Замены по преподавателю\n")
        if v_replacements not in ["1", "2", "exit"]:
            print("Неверная опция.")
            self.__replacements()
            return
        if v_replacements == "1":
            print(f"Замены на сегодня: {self.__get_today_replacements()}")
        elif v_replacements == "2":
            while True:
                teacher = self.__smart_input("Наберите имя учителя, для которого ищется замена: ")
                if self.__check_teacher_name(teacher):
                    break
                else:
                    print("Неверный учитель.")
            print(f"Замены на сегодня для учителя {teacher}: {self.__get_replacements_by_teacher(teacher)}")

    def __holidays(self):
        try:
            choice = int(self.__smart_input('1. Выбора нужного года\n'
                                            '2. Ближайшие каникулы\n'))
        except ValueError:
            self.__holidays()
            return

        if choice == 1:
            year = int(self.__smart_input('Введите нужный год.\n'))
            if not self.__check_year(year):
                while not self.__check_year(year):
                    year = int(self.__smart_input('Неверный ввод. Попробуйте ввести год снова.\n'))
            print(self.__get_holidays_for_year(year))
        elif choice == 2:
            print(self.__get_near_holidays())
        else:
            print('Неверная опция!')
            self.__holidays()

    def __my_next_lesson(self):
        current_datetime = datetime.datetime.now()
        closest_lesson = self.__get_closest_lesson_for_current_student(current_datetime)
        print(f'Ваш ближайший урок сегодня:\n{closest_lesson}')

    def __get_class_teacher(self):
        student_name = self.__smart_input(
            'Введите полное ФИО ученика по которому хотите получить информацию о классруке: ')
        if not self.__check_student_name(student_name):
            print('Неверное имя ученика!')
            self.__get_class_teacher()
        print('Информация об учителе:\n'
              f'{self.__get_teacher_info_by_student(student_name)}')

    def __teacher_info(self):
        teacher_name = self.__smart_input('Введите ФИО учителя в формате И. О. Фамилия: ')
        if not self.__check_teacher_name(teacher_name):
            print(f'{teacher_name} не настоящее имя!')
            self.__teacher_info()
        option = self.__smart_input('Что сделать? 1. где находится кабинет учителя 2. расписание по учителю: ')
        if option == '1':
            print(f'{self.__get_teacher_classroom(teacher_name)}')
        elif option == '2':
            print(f'\n{self.__get_teacher_schedule(teacher_name)}')
        else:
            print('Неверная опция!')
            self.__teacher_info()

    def __get_teacher_info_by_student(self, student_name):
        # TODO: пофиксить, если несколько учеников с одним фио это не будет работать
        group_list = StudentsForGroups.get_group_by_student_id(
            Student.get_by_name(student_name, self.__db_source)[0].get_main_id(), self.__db_source)
        teacher_id = None
        for i in group_list:
            if not i.get_letter().isdigit():
                teacher_id = i.get_teacher_id()
                break

        teacher_obj = Teacher.get_by_id(teacher_id, self.__db_source)
        name = teacher_obj.get_fio()
        contacts = teacher_obj.get_contacts()
        classroom = Location.get_by_id(teacher_obj.get_office_id(), self.__db_source).get_num_of_class()

        data = [[name, contacts, classroom]]
        return tabulate(data, ['ФИО', 'Контакты', 'Кабинет'], tablefmt='grid')

    def __check_year(self, year):
        data = [timetable['object_id'] for timetable in
                self.__db_source.get_by_query('TimeTables', {'time_table_year': year})]
        if data:
            return True
        else:
            return False

    def __get_current_user_info(self, student_name):
        data = [(student['object_id'], student['full_name'], student['date_of_birth']) for student in
                self.__db_source.get_by_query('Students', {'full_name': student_name})]
        if len(data) == 1:
            return data[0][0], data[0][1]
        else:
            print('Найдено совпадение. Выберите ваш ID:')
            print(tabulate(data, ['ID', 'ФИО', 'дата рождения'], tablefmt='grid'))
            object_id = int(input())
            if self.__db_source.get_by_id('Students', object_id):
                return object_id, student_name

    def __check_student_name(self, student_name):
        # проверяет существование ученика с таким именем
        # db_result = self.__db_source.get_by_query("Students", {"full_name": student_name})
        # if len(db_result) == 0:
        #             return False
        #         return True
        try:
            db_result = Student.get_by_name(student_name, self.__db_source)
            return bool(db_result)
        except Exception as e:
            print(f'ошибка!!! {e}')
        return False

    def __get_holidays_for_year(self, year):  # вывод NoLearningPeriod, связ. с таймтеблом
        year_id = self.__db_source.get_by_query('TimeTables', {'time_table_year': year})[0]['object_id']
        data = self.__db_source.get_by_query('NoLearningPeriods', {'timetable_id': year_id})
        result = []
        for NoLR in data:
            result.append((NoLR['start_time'], NoLR['stop_time']))
        return tabulate(sorted(result), ['Начало каникул', 'Конец каникул'], tablefmt='grid')

    def __check_teacher_name(self, teacher_name):
        data = [teacher for teacher in self.__db_source.get_by_query('Teachers', {'fio': teacher_name})]
        if data:
            return True
        else:
            return False

    def __get_near_holidays(self):
        today = datetime.date.today()
        year_id = self.__db_source.get_by_query('TimeTables', {'time_table_year': today.year})[0]['object_id']
        data = self.__db_source.get_by_query('NoLearningPeriods', {'timetable_id': year_id})
        result = []
        for NoLR in data:
            if NoLR['start_time'] >= today or NoLR['stop_time'] >= today:
                result.append((NoLR['start_time'], NoLR['stop_time']))
        return tabulate(sorted(result), ['Начало каникул', 'Конец каникул'], tablefmt='grid')

    def __get_teacher_classroom(self, teacher_name: str):
        # возвращает кабинет в котором обитает учитель с таким именем
        teacher = Teacher.get_by_name(teacher_name, self.__db_source)
        if len(teacher) == 0:
            return f'Учителя с именем {teacher_name} не существует!'
        elif len(teacher) == 1:
            teacher = teacher[0]
        else:
            raise ValueError(f'Больше 1 учителя с именем {teacher_name}!')
        try:
            office_number = Location.get_by_id(teacher.get_office_id(), self.__db_source)
        except ValueError:
            raise ValueError(f'Офиса с ид {teacher.get_office_id()} (указан у объекта Teacher) не существует!')
        return f'Учитель {teacher_name} обычно бывает в {office_number.get_num_of_class()}'

    def __get_teacher_schedule(self, teacher_name):
        teacher = Teacher.get_by_name(teacher_name, self.__db_source)
        if len(teacher) == 0:
            return f"Учителя с именем {teacher_name} не существует "
        elif len(teacher) != 1:
            # while True:
            #     index = self.__smart_input('Кажется, оказалось несколько одинаковых вариантов. Выберите нужный!'
            #                                + tabulate({i + 1: teacher[i].get_fio() for i in range(len(teacher))}))
            #     if not index.isdigit() or not 0 >= int(index) - 1 >= len(teacher):
            #         print('Неверный ввод! Попробуйте еще раз!')
            #         continue
            #     teacher = teacher[int(index) - 1]
            #     break
            teacher = teacher[0]

        else:
            teacher = teacher[0]
        schedule = TeachersForLessonRows.get_lesson_rows_by_teacher_id(teacher.get_main_id(), self.__db_source)
        dict_schedule = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}

        # получает
        curr_year_id = TimeTable.get_by_year(year=datetime.date.today().year, db_source=self.__db_source).get_main_id()
        for i in schedule:
            if i.get_timetable_id() == curr_year_id:
                lesson_row_to_string = self.__lesson_row_to_string(i)
                dict_schedule[i.get_day_of_the_week() + 1].append(lesson_row_to_string)

            columns = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
            return tabulate(dict_schedule, headers=columns, tablefmt='grid')

        # возвращает расписание учителя с таким именем в виде таблицы, т.е. уже отформатированное

    def __get_closest_lesson_for_current_student(self, current_datetime: datetime.datetime):
        student_id = self.__current_user_id
        student_groups = StudentsForGroups.get_group_by_student_id(student_id, self.__db_source)
        lesson_rows_list: List[LessonRow] = []

        today = current_datetime.weekday()  # number 0-6
        current_timetable = TimeTable.get_by_year(self.__db_source)

        for i in student_groups:
            # надо бы переписать
            # здесь добавляются лессон_ровс если они из этого года и этого дня недели
            var = [j for j in i.get_lesson_rows() if
                   j.get_day_of_the_week() == today and j.get_timetable_id() == current_timetable.get_main_id()]
            if var:
                lesson_rows_list.append(*var)

        lesson_rows_list.sort(key=lambda x: x.get_start_time())
        if len(lesson_rows_list) == 0:
            return 'Сегодня уроков нет!'

        first_lesson_row = lesson_rows_list[0]

        weekday_to_text = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        return f'Ближайший урок сегодня, в {weekday_to_text[today]}: {self.__lesson_row_to_string(first_lesson_row)}'

    def __get_today_replacements(self):
        replacements = Lesson.get_today_replacements(date=datetime.date.today(), db_source=self.__db_source)
        return "замены на сегодняшний день\n" + tabulate([(i.get_date(), i.get_start_time(), i.get_end_time(),
                                                           Location.get_by_id(element_id=i.get_room_id(),
                                                                              db_source=self.__db_source)
                                                           .get_num_of_class(),
                                                           Teacher.get_by_id(element_id=i.get_teacher_id(),
                                                                             db_source=self.__db_source).get_fio())
                                                          for i in replacements],
                                                         ["Дата", "Начало урока", "Конец урока", "Номер кабинета",
                                                          "Заменяющий учитель"],
                                                         tablefmt='grid')

    def __check_lesson(self, lesson):  # нигде не используется ??? непонятно, что конкретно чекать
        return True

    def __check_day(self, day):  # то же самое, что с предыдущим чеком
        return True

    def return_schedule_for_today(self):
        return self.__get_schedule_for_today()

    def __get_schedule_for_today(self):
        # Узнаем, какой год нам надо смореть
        timetable_id = TimeTable.get_by_year(self.__db_source).get_main_id()
        # Берем все уроки, которые проходят сегодня
        lesson_rows = LessonRow.get_all_by_day(week_day=datetime.date.today().weekday(),
                                               db_source=self.__db_source)
        # Берем все замены, которые есть на сегодня
        lesson = {i.get_start_time(): i for i in Lesson.get_today_replacements(date=datetime.date.today(),
                                                                               db_source=self.__db_source)}
        # Смотрим группы, которые есть у ученика
        groups_id = [i.get_main_id() for i in Student.get_by_id(self.__current_user_id,
                                                                self.__db_source).get_all_groups()]
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
                                   self.__db_source).get_subject_name(),
                 Location.get_by_id(i.get_room_id(), self.__db_source).get_num_of_class())
                for i in lesson_rows_dct]
        if not data:
            return 'Сегодня уроков нет! Ура!'
        return f'Расписание на сегодня: {datetime.date.today()}\n' + \
               tabulate(data, ["Начало", "Конец", "Урок", "Кабинет"], tablefmt='grid')

    def __get_schedule_for_week(self):
        week_dict = {0: "Понедельник",
                     1: "Вторник",
                     2: "Среда",
                     3: "Четверг",
                     4: "Пятница",
                     5: "Суббота",
                     6: "Воскресенье"}

        for i in range(0, 6):
            print(f"\n{week_dict[i]}\n")
            print(tabulate(self.__get_schedule_for_day(i), ["Предмет", "Время начала", "Место проведения"],
                           tablefmt="grid"))
        return

    def __get_schedule_for_day(self, day):
        db_result = LessonRow.get_by_day_and_student(day, self.__current_user_id, self.__db_source)
        data = {"subj_names": [], "start_times": [], "locations": []}
        for lesson_row in db_result:
            data.get("subj_names").append(
                Subject.get_by_id(lesson_row.get_subject_id(), db_source=self.__db_source).get_subject_name())
            data.get("start_times").append(lesson_row.get_start_time())
            location = Location.get_by_id(lesson_row.get_room_id(), db_source=self.__db_source)
            if location.get_link() is None:
                data.get("locations").append(location.get_num_of_class())
            else:
                data.get("locations").append(location.get_link())
        return data

    def __get_replacements_by_teacher(self, teacher):
        replacements = Lesson.get_replacements_by_teacher(date=datetime.date.today(), db_source=self.__db_source,
                                                          teacher=teacher)
        res = [(i.get_start_time(), i.get_end_time(),
                Subject.get_by_id(i.get_subject_id(), db_source=self.__db_source).get_subject_name(),
                Location.get_by_id(i.get_room_id(), db_source=self.__db_source).get_num_of_class())
               for i in replacements]
        return "\n" + tabulate(res, ['Начало', "Конец", "Урок", "Кабинет"],
                               tablefmt='grid')

    def __smart_input(self, input_text):
        res = input(input_text)
        if res == 'exit' or res == 'выйти':
            # бесконечная, поэтому игнорим то что дальше будет что-то возвращено
            print('Возвращаюсь в главное меню...')
            self.main_loop()
        return res

    def __lesson_row_to_string(self, lesson_row: LessonRow) -> str:
        subject = Subject.get_by_id(lesson_row.get_subject_id(), self.__db_source).get_subject_name()
        room = Location.get_by_id(lesson_row.get_room_id(), self.__db_source).get_num_of_class()
        group = Group.get_by_id(lesson_row.get_group_id(), self.__db_source)
        group = str(group.get_grade()) + ' ' + group.get_letter()

        # TODO: if time == 1103, str will be 11:3 instead of 11:03. fix later!
        start_time = f'{lesson_row.get_start_time() // 100}:{lesson_row.get_start_time() % 100}{"0" if lesson_row.get_start_time() % 100 == 0 else ""}'
        end_time = f'{lesson_row.get_end_time() // 100}:{lesson_row.get_end_time() % 100}{"0" if lesson_row.get_end_time() % 100 == 0 else ""}'

        lesson_row_to_string = f'{subject.capitalize()} с {start_time} до {end_time} в каб. ' \
                               f'{room}\nс классом/группой {group}'
        return lesson_row_to_string
