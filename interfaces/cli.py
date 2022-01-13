from adapters.file_source import FileSource
from data_model.teacher import Teacher
from interfaces.user import User


# menu = [show_timetable, show_teachers, show_classes, get_user_info]

menu = '''
------------------------
please enter number from 1 to 4(we hope u r smart enough to enter numbers not names of ur friends like Anton
------------------------
[1] show_timetable
------------------------
[2] show_teachers
------------------------
[3] show_classes
------------------------
[4] get_user_info
------------------------
[5] exit
------------------------
'''


class CLI:
    def __init__(self, user: User, _db_source: FileSource):
        self.__db_source = _db_source  # проинициализировали Filesource, чтобы передать как параметр в get_all
        self.__identifier = [self.__show_timetable, self.__show_teachers, self.__show_classes, self.get_user_info]
        self.__user = user

    def __show_timetable(self):
        print(FileSource.get_all(self.__db_source, "Timetable"))

    def __show_classes(self):
        print(self.__db_source.get_all("Group"))

    def get_user_info(self):
        return f"status: {self.__user.get_access_level()}, user's class: {self.__user.get_class_of_user()}," \
               f"name: {self.__user.get_identity()[0]}, surname: {self.__user.get_identity()[1]}"

    def __show_teachers(self):
        print(FileSource.get_all(self.__db_source, "Teacher"))

    def show_menu(self):
        print(menu)
        choice = int(input())
        if choice == 5:
            return True
        else:
            print()
            print(self.__identifier[int(choice) - 1]())
            return False


print("Предьявите инфу о себе здесь:")
example = CLI(User(), FileSource("../db"))
while True:
    if example.show_menu():
        print("Всем пока!!!!!!")
        break
