import datetime
from tabulate import tabulate
from adapters.abstract_source import AbstractSource


class StudentInterface:
    def __init__(self, db_source: AbstractSource, student_id: int):
        self.__current_user_id = None
        self.__current_user = None
        self.__db_source = db_source
        self.__log = False
        self.__today = datetime.date.today()
        self.__current_year = self.__today.year
        self.__current_day_of_week = self.__today.weekday()  # передается от 0 до 6, нужно обсудить в каком формате у нас день недели в итоге
        self.__login()

    def __login(self):
        username = self.__smart_input('Ваше ФИО: ')
        if self.__check_student_name(username):
            self.__current_user_id, self.__current_user = self.__get_current_user_info(username)
            print(f'Успешно зашли под именем {username}!')
            self.__log = True
            self.main_loop()
        else:
            print(f'Такого ученика не существует.')
            self.__login()

    def __logout(self):
        self.__current_user = None
        self.__log = False
        print('Вы успешно вышли!')

    def main_loop(self):
        while self.__log:
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
                self.__log = False
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
        print(f'Ваш ближайший урок: {closest_lesson}')

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
            print(f'Кабинет учителя: {self.__get_teacher_classroom(teacher_name)}')
        elif option == '2':
            print(f'Расписание учителя: {self.__get_teacher_schedule(teacher_name)}')
        else:
            print('Неверная опция!')
            self.__teacher_info()

    def __get_teacher_info_by_student(self, student_name):
        # возвращает фио учителя-классрука для ученика у которого такое имя
        try:
            student_id = self.__db_source.get_by_query('Students', {'full_name': student_name})[0]['object_id']
        except IndexError:
            raise ValueError('Введено неправильное имя.')
        SFGs = self.__db_source.get_by_query('StudentsForGroups', {'student_id': student_id})
        for SFG in SFGs:
            grps = self.__db_source.get_by_query('Groups', {'object_id': SFG['group_id']})
            for grp in grps:
                LRs = self.__db_source.get_by_query('LessonRows', {'group_id': grp['object_id']})
                for LR in LRs:
                    TforLRs = self.__db_source.get_by_query('TeachersForLessonRows', {'lesson_row_id': LR['object_id']})
                    for TforLR in TforLRs:
                        teachers = self.__db_source.get_by_query('Teachers', {'object_id': TforLR['teacher_id']})
        data = []
        try:
            for teacher in teachers:
                data.append((teacher['fio'], teacher['contacts'],
                             self.__db_source.get_by_id('Locations', teacher['office_id'])['num_of_class']))
        except UnboundLocalError:
            raise ValueError('У данного ученика нет классного руководителя.')
        return tabulate(data, ['ФИО', 'Контакты', 'Кабинет'], tablefmt='grid')

    def __check_year(self, year):
        data = [timetable['object_id'] for timetable in self.__db_source.get_by_query('TimeTables', {'time_table_year': year})]
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
        data = [student for student in self.__db_source.get_by_query('Students', {'full_name': student_name})]
        if data:
            return True
        else:
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

    def __get_teacher_classroom(self, teacher_name):
        # возвращает кабинет в котором обитает учитель с таким именем
        return f'кабинет номер 00000 учителя {teacher_name}'

    def __get_teacher_schedule(self, teacher_name):
        # возвращает расписание учителя с таким именем в виде таблицы, т.е. уже отформатированное
        return f'<тестовое расписание учителя {teacher_name}>'

    def __get_closest_lesson_for_current_student(self, current_datetime: datetime.datetime):
        return f'<Ближайший урок от настоящего момента ({current_datetime.strftime("%b %d %Y %H:%M:%S")})>' \
               f' - от учителя X, в кабинете N, время проведения: K'

    def __get_today_replacements(self):
        # замены на сегодня для определенного ученика (который щас залогинен)
        return "замены на сегоднешний день"

    def __check_lesson(self, lesson):  # нигде не используется ??? непонятно, что конкретно чекать
        return True

    def __check_day(self, day):  # то же самое, что с предыдущим чеком
        return True

    def __get_schedule_for_today(self):
        return 'расписание на сегодня'

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
