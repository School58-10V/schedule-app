from adapters.file_source import FileSource
from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from tabulate import tabulate

fs = FileSource('../db')
TfS = TeachersForLessonRows(fs, 0, 0)


class CLI:
    def __init__(self):
        self.tasks = {1: "1. показать всех учителей", 2: "2. показать список всех преподаваемых предметов",
                      3: "3. показать всех учеников школы", 4: "4. показать расписание"}

    def show_menu(self):
        print('Меню:', 'Список команд.', sep='\n')
        print(*[self.tasks[i] for i in range(1, len(self.tasks) + 1)], sep="\n", end='\n')
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
        all_teachers = fs.get_all('Teacher')
        for teacher in all_teachers:
            del teacher['object_id']
        print(*[teacher for teacher in all_teachers], sep='\n')
        self.show_menu()

    def __show_all_subjects(self):
        all_subject = fs.get_all('Subject')
        for subject in all_subject:
            del subject['object_id']
        print(*[subject for subject in all_subject], sep='\n')
        self.show_menu()

    def __show_all_students(self):
        all_student = fs.get_all('Student')
        for student in all_student:
            del student['object_id']
        print(*[student for student in all_student], sep='\n')
        self.show_menu()

    def __show_timetable(self):
        subjects = fs.get_all('LessonRow')
        column_list = ['day_of_the_week', 'teacher', 'group', 'subject', 'room',
                       'start_time', 'end_time']
        value_list = []
        for subject in subjects:
            new_list = []
            for title in column_list:
                for elem in subject:
                    if title in elem:
                        if 'id' in elem and title != 'room':
                            object = fs.get_by_id(title.capitalize(), subject[elem])
                            if title == 'group':
                                teachers = [teacher.__dict__() for teacher in
                                            TfS.get_teachers_by_lesson_row_id(subject['object_id'], fs)]
                                for teacher in teachers:
                                    del teacher['object_id']
                                new_list.append(teachers)
                                del object['teacher_id']
                            del object['object_id']
                            new_list.append(object)
                        else:
                            new_list.append(subject[elem])
            value_list.append(new_list)
        print(tabulate(self.sort_days_of_the_week(value_list), column_list, tablefmt='grid'))
        self.show_menu()


    @staticmethod
    def sort_days_of_the_week(dicts) -> list[dict]:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        monday = []
        tuesday = []
        wednesday = []
        thursday = []
        friday = []
        for dct in dicts:
            if dct[0] == days[0]:
                monday.append(dct)
            elif dct[0] == days[1]:
                tuesday.append(dct)
            elif dct[0] == days[2]:
                wednesday.append(dct)
            elif dct[0] == days[3]:
                thursday.append(dct)
            elif dct[0] == days[4]:
                friday.append(dct)
        return monday + tuesday + wednesday + thursday + friday
