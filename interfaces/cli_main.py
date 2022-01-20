from tabulate import tabulate

from adapters.file_source import FileSource
from data_model.student import Student
from data_model.subject import Subject
from data_model.teacher import Teacher
from data_model.lesson_row import LessonRow
from data_model.students_for_groups import StudentsForGroups


class CLI:
    def __init__(self, name: str = None, user_type: str = None):
        self.user_type = user_type
        self.name = name
        self.db_adapter = FileSource()

    def set_database_path(self, path):
        self.db_adapter = FileSource(path)

    def __pretty_print(self, *args, **kwargs):
        print(*args, **kwargs)

    def get_info(self):
        self.__pretty_print("Ввидите данные:")
        self.user_type = input("Ваш вид дейтельности (учитель/ученик/администратор):")
        while self.user_type != "учитель" and self.user_type != "ученик" and self.user_type != "администратор":
            self.user_type = input("такого типа нет, выберите 'учитель' или 'ученик' или 'администратор'")
        self.name = input("ФИО")

    def __menu_for_student(self, action):
        if action == 1:
            self.__get_schedule_by_student()
        elif action == 2:
            self.__get_all_teachers()

    def __menu_for_teacher(self, action):
        if action == 1:
            self.__schedule_by_teacher()
        elif action == 2:
            self.__schedule_changes_by_teacher()
        elif action == 3:
            self.__add_new_subject()

    def __menu_for_admin(self, action):
        if action == 1:
            self.__add_new_teacher_menu()
        elif action == 2:
            self.__add_new_student_menu()
        elif action == 3:
            self.__add_new_schedule_change()
        elif action == 4:
            self.__add_new_lesson_row()

    def show_menu(self):
        if not self.name:
            self.get_info()
        while True:
            self.__pretty_print("Выберите действие по типу (или exit если хотите выйти): ")
            if self.user_type == "учитель":
                prompt = ["расписание (уроки и группы на этих уроках)", "замены", "добавить новый предмет"]
            elif self.user_type == "администратор":
                prompt = ["добавить учителя", "добавить ученика", "добавить замены", "добавить новый ряд уроков"]
            elif self.user_type == 'ученик':
                prompt = ["расписание (уроки и групы на этих уроках)", "все учителя"]

            action = input('\n'.join([f'{i + 1}. {prompt[i]}' for i in range(len(prompt))]) + '\n')
            if action == 'exit':
                self.__pretty_print(f'До новых встреч, {self.name}!')
                break
            while action not in [str(i) for i in range(1, len(prompt) + 1)]:
                action = input('Неверный ввод данных, попробуйте еще раз')
            action = int(action)
            if self.user_type == "учитель":
                self.__menu_for_teacher(action)
            elif self.user_type == "администратор":
                self.__menu_for_admin(action)
            elif self.user_type == 'ученик':
                self.__menu_for_student(action)

    def __add_new_teacher_menu(self):
        new_teacher_name = input('Имя нового учителя: ')
        self.__add_new_teacher(new_teacher_name)
        self.__pretty_print('Готово!')

    def __add_new_teacher(self, teacher_name):
        t = Teacher(self.db_adapter, teacher_name)
        t.save()

    def __add_new_student_menu(self):
        new_student_name = input('Имя нового ученика: ')
        new_student_date_of_birth = input('Дата рождения нового учителя: ')
        self.__add_new_student(new_student_name, new_student_date_of_birth)
        self.__pretty_print('Готово!')

    def __add_new_student(self, new_student_name, new_student_date_of_birth):
        s = Student(self.db_adapter, new_student_name, new_student_date_of_birth)
        s.save()

    def __show_all_teachers(self):
        all_teachers = self.__get_all_teachers()
        column_list = ['ФИО', 'БИО', 'контакты', 'Кабинет']
        value_list = []
        for teacher in all_teachers:
            value_list.append([teacher.get_fio(), teacher.get_bio(), teacher.get_contacts(), teacher.get_office_id()])
        print(tabulate(sorted(value_list, key=lambda elem: elem[2]), column_list,
                       tablefmt='grid'))  # сортировка по био (чтобы сначала все учителя математики были, потом етс)

    def __get_all_teachers(self):
        return Teacher.get_all(self.db_adapter)

    def __add_new_subject(self):
        new_subject_name = input('Имя нового предмета: ')
        s = Subject(self.db_adapter, new_subject_name)
        s.save()
        self.__pretty_print('Готово!')

    def __add_new_lesson_row(self):
        start_time = int(input('начало урока:'))
        end_time = int(input('конец урока:'))
        count_studying_hours = int(input('количество академических часов в занятии:'))
        room_id = int(input('айди комнаты:'))
        group_id = int(input('группа учеников:'))
        subject_id = int(input('предмет:'))
        timetable_id = int(input('год в который происходят уроки:'))
        day_of_week = int(input('номер дня недели:'))
        s = LessonRow(self.db_adapter, count_studying_hours, group_id, subject_id, room_id, start_time, end_time,
                      timetable_id, day_of_week)
        s.save()
        self.__pretty_print('Готово!')

    def __schedule_by_teacher(self):
        pass

    def __schedule_changes_by_teacher(self):
        pass

    def __get_schedule_by_student(self):
        student = [i for i in Student.get_all(self.db_adapter) if i.get_full_name() == self.name][0]
        day = []
        for i in StudentsForGroups.get_group_by_student_id(student.get_main_id(), self.db_adapter):
            for x in [j for j in LessonRow.get_all(self.db_adapter) if
                      j.get_timetable_id() == self.year and j.get_day_of_week() == self.day_of_weeks and j.get_group_id() == i.get_main_id()]:
                day.append(x)
        self.__pretty_print('\n'.join([
                                          f'{Student.get_by_id(i.get_subject_id(), self.db_adapter).get_subject_name()} начало урока: {str(i.get_start_time())[:-2]}:{str(i.get_start_time())[2:]} конец урока: {str(i.get_end_time())[:-2]}:{str(i.get_end_time())[2:]}'
                                          for i in sorted(day, key=lambda y: y.get_end_time())]))
        self.__pretty_print('Готово!')

    def __add_new_schedule_change(self):
        pass


# cli = CLI('Хромов Михаил', 'ученик')
cli = CLI()
cli.set_database_path('../db/')
cli.show_menu()
