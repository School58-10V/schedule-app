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
        return f"status:{self.__user}, user's class:{self._class_of_user}, name:{self._name}, " \
               f"surname:{self._surname}"

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
example = CLI(input("Ваш статус в иерхахии:").lower(),
              input("Ваш класс(если вы студент):").upper(),
              input("Ваше имя:").lower(),
              input("Ваша фамилия:").lower(), FileSource("../db"))
boyyyyyy = Teacher(FileSource("../db"), "уцпйкк232", bio="сидел 3 года")
boyyyyyy.save()
while True:
    if example.show_menu():
        print("Всем пока!!!!!!")
        break
