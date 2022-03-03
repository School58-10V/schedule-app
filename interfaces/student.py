import datetime


class StudentInterface:
    def __init__(self):
        self.current_user = None

    def login(self):
        username = input('Ваше ФИО: ')
        if self.__check_student_name(username):
            self.current_user = username
            print(f'Успешно зашли под именем {username}!')
        else:
            print(f'Такого ученика не существует.')

    def logout(self):
        self.current_user = None
        print('Вы успешно вышли!')

    def main_loop(self):
        while True:
            print()
            if not self.current_user:
                self.login()
                continue
            option = input('Выберете опцию:\n'
                           '1. Информация о учителе\n'
                           '2. Узнать классного руководителя ученика\n'
                           '3. Мое следующее занятие\n'
                           '4. Информация о каникулах\n'
                           '5. Информация о заменах\n'
                           '6. Расписание\n'
                           '9. Выйти из аккаунта\n'
                           'Ваша опция: ')
            if option == '1':
                self.teacher_info()
            elif option == '2':
                self.get_class_teacher()
            elif option == '3':
                self.my_next_lesson()
            elif option == '4':
                self.holidays()
            elif option == '5':
                self.replacements()
            elif option == '6':
                self.schedule()
            elif option == '9':
                self.logout()
            else:
                print('Неверная опция!')

    def schedule(self):
        option = int(input('''
Напишите 1 - чтобы посмотреть расписание на сегодня
Напишите 2 - чтобы посмотреть расписание на неделю
Напишите 3 - чтобы посмотреть расписание на какой-либо день '''))
        while option != 1 and option != 2 and option != 3:
            option = int(input('Введите коректное число'))

        if option == 1:
            return self.__get_schedule_for_today()
        elif option == 2:
            return self.__get_schedule_for_week()
        elif option == 3:
            day = int(input('''
Напишите день на котороый хотите посмотреть расписание
Понедельник - 1
Вторник - 2
 т.д.'''))
            self.__get_schedule_for_day(day)

    def replacements(self):
        v_replacements = input("Выбирите опцию: 1. Замена на сегоднишний день 2. Выбирите замену по предмету, дате, преподователю")
        while True:
            if v_replacements in ["1", "2"]:
                break
            else:
                print("Неверная опция.")
        if v_replacements == "1":
            print(f"Замены на сегодня{self.__today_replacements()}")
        elif v_replacements == "2":
            lesson = input("Выбирите предмет, для которого ищется замена (Если этот пораметр вас не интересует запишите '-'):")
            while True:
                if self.__check_lesson(lesson):
                    break
                else:
                    print("Неверный предмет.")
                    lesson = input("Выбирите предмет, для которого ищется замена (Если этот пораметр вас не интересует запишите '-'):")
            teacher = input("Выбирите учителя, для которого ищется замена (Если этот пораметр вас не интересует запишите '-'):")
            while True:
                if self.__check_teacher(teacher):
                    break
                else:
                    print("Неверный учитель.")
                    teacher = input("Выбирите учителя, для которого ищется замена (Если этот пораметр вас не интересует запишите '-'):")
            day = input("Выбирите день, для которого ищется замена (Если этот пораметр вас не интересует запишите '-'):")
            while True:
                if self.__check_day(day):
                    break
                else:
                    print("Неверный день.")
                    day = input("Выбирите день, для которого ищется замена (Если этот пораметр вас не интересует запишите '-'):")
            print(f"Замены на {day}: {self.__day_replacements(lesson, teacher, day)}")

    def holidays(self):
        try:
            choice = int(input('1. Выбора нужного года\n'
                               '2. Ближайшие каникулы\n'))
        except ValueError:
            print('Неверная опция!')
            return

        if choice == 1:
            year = int(input('Введите нужный год.\n'))
            if not self.__check_year(year):
                while not self.__check_year(year):
                    year = int(input('Неверный ввод. Попробуйте ввести год снова.\n'))
            print(self.__get_holidays_for_year(year))
        elif choice == 2:
            print(self.__get_near_holidays())
        else:
            print('Неверная опция!')

    def my_next_lesson(self):
        current_datetime = datetime.datetime.now()
        closest_lesson = self.__get_closest_lesson_for_current_student(current_datetime)
        print(f'Ваш ближайший урок: {closest_lesson}')

    def get_class_teacher(self):
        student_name = input('Введите полное ФИО ученика по которому хотите получить информацию о классруке: ')
        if not self.__check_student_name(student_name):
            print('Неверное имя ученика!')
            return
        print(f'Информация об учителе: {self.__get_teacher_info_by_student(student_name)}')

    def teacher_info(self):
        teacher_name = input('Введите ФИО учителя в формате И. О. Фамилия: ')
        if not self.__check_teacher_name(teacher_name):
            print(f'{teacher_name} не настоящее имя!')
            return
        option = input('Что сделать? 1. где находится кабинет учителя 2. расписание по учителю: ')
        if option == '1':
            print(f'Кабинет учителя: {self.__get_teacher_classroom(teacher_name)}')
        elif option == '2':
            print(f'Расписание учителя: {self.__get_teacher_schedule(teacher_name)}')
        else:
            print('Неверная опция!')

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

    def __today_replacements(self):
        return "замены на сегоднешний день"


    def __check_lesson(self, lesson):
        return True

    def __check_teacher(self, teacher):
        return True

    def __check_day(self, day):
        return True


a = StudentInterface()
a.main_loop()
