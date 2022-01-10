from adapters.file_source import FileSource
from tabulate import tabulate

fs = FileSource('../db')


class CLI:
    def __init__(self):
        self.tasks = {1: "1. показать всех учителей", 2: "2. показать список всех преподаваемых предметов",
                      3: "3. показать всех учеников школы", 4: "4. показать расписание"}

    def show_menu(self):
        print('Меню:'
              'Список команд.')
        print([self.tasks[i] for i in range(1, len(self.tasks) + 1)], sep="\n")
        print("Выберите номер нужной команды из списка или введите 0 для окончания работы с интерфейсом.")
        number = int(input())
        if number:
            if number == 1:
                self.__show_all_teachers()
            if number == 2:
                self.__show_all_subjects()
            if number == 3:
                self.__show_all_students()
            if number == 4:
                self.__show_timetable()
        else:
            return

    def __show_all_teachers(self):
        print(fs.get_all('Teacher'))
        self.show_menu()

    def __show_all_subjects(self):
        print(fs.get_all('Subject'))
        self.show_menu()

    def __show_all_students(self):
        print(fs.get_all('Student'))
        self.show_menu()

    def __show_timetable(self):
        subjects = fs.get_all('LessonRow')
        column_list = ['count_studying_hours', 'group', 'subject', 'room',
                       'start_time', 'end_time']
        value_list = []
        for subject in subjects:
            new_list = []
            for title in column_list:
                for elem in subject:
                    if title in elem:
                        if 'id' in elem and title != 'room':
                            new_list.append(fs.get_by_id(title.capitalize(), subject[elem]))
                        else:
                            new_list.append(subject[elem])
            value_list.append(new_list)
        print(tabulate(value_list, column_list, tablefmt='grid'))
        self.show_menu()
