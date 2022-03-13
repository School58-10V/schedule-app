import datetime

from tabulate import tabulate
from adapters.abstract_source import AbstractSource
from data_model.lesson import Lesson
from data_model.lesson_row import LessonRow
from db_source import DBSource


class StudentInterface:
    days = ['Понедельник', "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

    def __init__(self, db_source: AbstractSource, student_id: int):
        self.__current_user_id = student_id
        self.__current_user = str(student_id)  # TODO: сделать это именем, т.е. получить имя студента через БД
        self.__db_source = db_source
        self.__student_id = 1010
        self.__current_year = 2022
        self.__current_day_of_week = 'mon'

    def __login(self):
        username = self.__smart_input('Ваше ФИО: ')
        if self.__check_student_name(username):
            self.__current_user = username
            print(f'Успешно зашли под именем {username}!')
        else:
            print(f'Такого ученика не существует.')

    def __logout(self):
        self.__current_user = None
        print('Вы успешно вышли!')

    def main_loop(self):
        while True:
            print()
            print(tabulate([(1, "Информация о учителе"),
                            (2, "Узнать классного руководителя ученика"),
                            (3, "Мое следующее занятие"),
                            (4, "Информация о каникулах"),
                            (5, "Информация о заменах"),
                            (6, "Расписание"),
                            (0, "Выйти из аккаунта")], ['Опция', 'Команда'], tablefmt='grid'))
            option = self.__smart_input('Ваша опция (используйте exit чтобы в любой момент выйти в главное меню): ')
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
            else:
                print('Неверная опция!')

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
            print(self.__get_schedule_for_week())
        elif option == 3:
            day = int(self.__smart_input('''
Напишите день на котороый хотите посмотреть расписание
Понедельник - 1
Вторник - 2
 т.д.'''))
            print(self.__get_schedule_for_day(day))

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
                teacher = self.__smart_input("Выбирите учителя, для которого ищется замена: ")
                if self.__check_teacher(teacher):
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
        print(f'Ваш ближайший урок: {closest_lesson}')

    def __get_class_teacher(self):
        student_name = self.__smart_input(
            'Введите полное ФИО ученика по которому хотите получить информацию о классруке: ')
        if not self.__check_student_name(student_name):
            print('Неверное имя ученика!')
            self.__get_class_teacher()
        print(f'Информация об учителе: {self.__get_teacher_info_by_student(student_name)}')

    def __teacher_info(self):
        teacher_name = self.__smart_input('Введите ФИО учителя в формате И. О. Фамилия: ')
        if not self.__check_teacher_name(teacher_name):
            print(f'{teacher_name} не настоящее имя!')
            self.__teacher_info()
        option = self.__smart_input('Что сделать? 1. где находится кабинет учителя 2. расписание по учителю: ')
        if option == '1':
            print(f'Кабинет учителя: {self.__get_teacher_classroom(teacher_name)}')
        elif option == '2':
            print(f'Расписание учителя: {self.__get_teacher_schedule(teacher_name)}')
        else:
            print('Неверная опция!')
            self.__teacher_info()

    def __get_teacher_info_by_student(self, student_name):
        # возвращает фио учителя-классрука для ученика у которого такое имя
        return f'<классрук ученика {student_name}>'

    def __check_year(self, year):  # проверка на наличие timetable на год
        return True

    def __check_student_name(self, student_name):
        # проверяет существование ученика с таким именем
        return True

    def __get_holidays_for_year(self, year):  # вывод NoLearningPeriod, связ. с таймтеблом
        return f'каникулы на {year} год'

    def __check_teacher_name(self, teacher_name):
        # проверяет существование учителя с таким именем
        return True

    def __get_near_holidays(self):
        day = datetime.date.today()
        return f'следующие каникулы с {day}'

    def __get_teacher_classroom(self, teacher_name):
        # возвращает кабинет в котором обитает учитель с таким именем
        return f'кабинет номер 00000 учителя {teacher_name}'

    def __get_teacher_schedule(self, teacher_name):
        # возвращает расписание учителя с таким именем в виде таблицы, т.е. уже отформатированное
        return f'<тестовое расписание учителя {teacher_name}>'

    def __get_closest_lesson_for_current_student(self, current_datetime: datetime.datetime):
        return f'<Ближайший урок от настоящего момента ({current_datetime.strftime("%b %d %Y %H:%M:%S")})>' \
               f' - от учителя X, в кабинете N, время проведения: K'

    @staticmethod
    def __get_today_replacements(db_source: DBSource):
        replacements = Lesson.get_today_replacements(date=datetime.date.today(), db_source=db_source)
        return "замены на сегодняшний день\n" + tabulate([i for i in replacements])

    def __check_lesson(self, lesson):
        return True

    def __check_teacher(self, teacher):
        return True

    def __check_day(self, day):
        return True

    def __get_schedule_for_today(self, db_source: DBSource):
        lesson_rows = LessonRow.get_all_by_day(week_day=self.days[datetime.date.today().weekday()],
                                               db_source=db_source)
        lesson = {i.get_start_time(): i for i in Lesson.replacements(datetime.date.today())}
        lesson_rows_dct = []
        for i in lesson_rows:
            lesson_rows_dct.append(i if i.get_start_time() not in lesson else lesson[i.get_start_time()])
        # lesson_rows_dct = {i.get_start_time(): i for i in lesson_rows if i.get_start_time() not in lesson else
        # lesson[i]}
        lesson_rows_dct.sort(key=lambda x: x.get_start_time())
        return 'Расписание на сегодня\n' + tabulate(
                [(i.get_start_time(), i.get_end_time(), i.get) for i in lesson_rows_dct])

    def __get_schedule_for_week(self):
        return 'расписание на эту неделю'

    def __get_schedule_for_day(self, day):
        return f'расписание на день {day}'

    def __get_replacements_by_teacher(self, teacher):
        return f'заменя для учителя {teacher} на сегодня'

    def __smart_input(self, input_text):
        res = input(input_text)
        if res == 'exit':
            # бесконечная, поэтому игнорим то что дальше будет что-то возвращено
            print('Возвращаюсь в главное меню...')
            self.main_loop()
        return res
