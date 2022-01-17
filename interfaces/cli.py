from operator import itemgetter

from data_model.teacher import Teacher
from data_model.lesson_row import LessonRow
from data_model.subject import Subject
from data_model.group import Group
from data_model.student import Student
from adapters.file_source import FileSource
from tabulate import tabulate


class CLI:
    def __init__(self, db_path):
        self.db_source = FileSource(db_path)
        self.tasks = {1: "1. показать всех учителей", 2: "2. показать список всех преподаваемых предметов",
                      3: "3. показать всех учеников школы", 4: "4. показать расписание"}

    def show_menu(self):
        print('Меню:', 'Список команд.', sep='\n')
        print(*[self.tasks[number] for number in range(1, len(self.tasks) + 1)], sep="\n", end='\n')
        print("Выберите номер нужной команды из списка или введите 0 для окончания работы с интерфейсом.")
        number = input()
        while str(number) not in ['0', '1', '2', '3', '4']:
            number = input('Неверный ввод данных, попробуйте еще раз')
        if number == '1':
            self.__show_all_teachers()
        elif number == '2':
            self.__show_all_subjects()
        elif number == '3':
            self.__show_all_students()
        elif number == '4':
            self.__show_timetable()
        elif number == '0':
            return

    def __show_all_teachers(self):
        all_teachers = Teacher.get_all(self.db_source)
        column_list = ['ФИО', 'БИО', 'контакты', 'Кабинет']
        value_list = []
        for teacher in all_teachers:
            value_list.append([teacher.get_fio(), teacher.get_bio(), teacher.get_contacts(), teacher.get_office_id()])
        print(tabulate(sorted(value_list, key=lambda elem: elem[2]), column_list, tablefmt='grid')) # сортировка по био (чтобы сначала все учителя математики были, потом етс)
        self.show_menu()

    def __show_all_subjects(self):
        all_subject = Subject.get_all(self.db_source)
        column_list = ['Название предмета']
        value_list = []
        for subject in all_subject:
            value_list.append([subject.get_subject_name()])
        print(tabulate(sorted(value_list), column_list, tablefmt='grid'))
        self.show_menu()

    def __show_all_students(self):
        all_student = Student.get_all(self.db_source)
        column_list = ['ФИО', 'Дата рождения', 'Контакты', 'Био', 'Группы ученика']
        value_list = []
        for student in all_student:
            value_list.append([student.get_full_name(), student.get_date_of_birth(), student.get_contacts(), student.get_bio(), '\n'.join([f'Цифра={group.get_grade()}, буква={group.get_letter()}, профиль={group.get_profile_name()}' for group in student.get_all_groups()])])
        print(tabulate(sorted(value_list, key=lambda elem: elem[4]), column_list, tablefmt='grid'))
        self.show_menu()

    def __show_timetable(self):
        subjects = LessonRow.get_all(self.db_source)
        column_list = ['День недели', 'Учитель', 'Класс/Группа', 'Предмет', 'Кабинет',
                       'Начало урока', 'Конец урока']
        value_list = []
        for subject in subjects:
            value_list.append([subject.get_day_of_the_week(),
                               '\n'.join([f'ФИО={teacher.get_fio()}, био={teacher.get_bio()}, контакты={teacher.get_contacts()}, кабинет={teacher.get_office_id()}' for teacher in subject.get_teachers()]),
                               f'Цифра={Group.get_by_id(subject.get_group_id(), self.db_source).get_grade()}, буква={Group.get_by_id(subject.get_group_id(), self.db_source).get_letter()}, профиль={Group.get_by_id(subject.get_group_id(), self.db_source).get_profile_name()}',
                               Subject.get_by_id(subject.get_subject_id(), self.db_source).get_subject_name(), subject.get_room_id(),
                               subject.get_start_time(), subject.get_end_time()])
        print(tabulate(self.sort_days_of_the_week(value_list), column_list, tablefmt='grid'))
        self.show_menu()

    def restart_menu(self):
        self.show_menu()

    @staticmethod
    def sort_days_of_the_week(lesson_rows) -> list:
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
        monday = []
        tuesday = []
        wednesday = []
        thursday = []
        friday = []
        for lesson_row in lesson_rows:
            if lesson_row[0] == days[0]:
                monday.append(lesson_row)
            elif lesson_row[0] == days[1]:
                tuesday.append(lesson_row)
            elif lesson_row[0] == days[2]:
                wednesday.append(lesson_row)
            elif lesson_row[0] == days[3]:
                thursday.append(lesson_row)
            elif lesson_row[0] == days[4]:
                friday.append(lesson_row)
        return  CLI.sort_by_start_time(monday) + CLI.sort_by_start_time(tuesday) + CLI.sort_by_start_time(
            wednesday) + CLI.sort_by_start_time(thursday) + CLI.sort_by_start_time(friday)

    @staticmethod
    def sort_by_start_time(day):
        return sorted(day, key=itemgetter(2, 5))

