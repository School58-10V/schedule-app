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
                self.free_days()
            elif option == '5':
                self.replacements()
            elif option == '6':
                self.schedule()
            elif option == '9':
                self.logout()
            else:
                print('Неверная опция!')

    def schedule(self):
        pass

    def replacements(self):
        pass

    def free_days(self):
        pass

    def my_next_lesson(self):
        pass

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

    def __check_student_name(self, student_name):
        # проверяет существование ученика с таким именем
        return True

    def __check_teacher_name(self, teacher_name):
        # проверяет существование учителя с таким именем
        return True

    def __get_teacher_classroom(self, teacher_name):
        # возвращает кабинет в котором обитает учитель с таким именем
        return f'кабинет номер 00000 учителя {teacher_name}'

    def __get_teacher_schedule(self, teacher_name):
        # возвращает расписание учителя с таким именем в виде таблицы, т.е. уже отформатированное
        return f'<тестовое расписание учителя {teacher_name}>'


a = StudentInterface()
a.main_loop()
