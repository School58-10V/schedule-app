from adapters.file_source import FileSource
from data_model.teacher import Teacher


menu = '''------------------------
please enter number from 1 to 4(we hope u r smart enough to enter numbers not names of ur friends like Anton
------------------------
[1] show_timetable
------------------------
[2] show_teachers
------------------------
[3] show_classes
------------------------
[4] get_user_info
------------------------'''


class CLI:
    def __init__(self, user_status: str, class_of_user: str, name: str, surname: str, _db_source: FileSource):
        self._db_source = _db_source  # проинициализировали Filesource, чтобы передать как параметр в get_all
        self._user_status = user_status
        self._class_of_user = class_of_user
        self._name = name
        self._surname = surname
        self.identifier = [self.__show_timetable(), self.__show_teachers(), self.__show_classes(), self.get_user_info()]

    def __show_timetable(self):
        print(FileSource.get_all(self._db_source, "Timetable"))

    def __show_classes(self):
        print(FileSource.get_all(self._db_source, "Group"))

    def get_user_info(self):
        return f"status:{self._user_status}, user's class:{self._class_of_user}, name:{self._name}, " \
               f"surname:{self._surname}"

    def __show_teachers(self):
        print(FileSource.get_all(self._db_source, "Teacher"))

    def show_menu(self):
        print(menu)
        choice = input()
        print(self.identifier[int(choice) - 1])


print("Предьявите инфу о себе здесь:")
example = CLI(input("Ваш статус в иерхахии:").lower(),
              input("Ваш класс(если вы студент):").upper(),
              input("Ваше имя:").lower(),
              input("Ваша фамилия:").lower(), FileSource())
boyyyyyy = Teacher(FileSource(), "уцпйкк232", bio="сидел 3 года")
boyyyyyy.save()
example.show_menu()

