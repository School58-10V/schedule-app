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
    def __init__(self, user_status: str, class_of_user: str, name: str, surname: str):
        self._user_status = user_status
        self._class_of_user = class_of_user
        self._name = name
        self._surname = surname
        self.identifier = [self.__show_timetable(), self.__show_teachers(), self.__show_classes(), self.get_user_info()]
        self.__logged_in = False

    def __show_timetable(self):
        pass

    def __show_classes(self):
        pass

    def get_user_info(self):
        return f"status:{self._user_status}, user's class:{self._class_of_user}, name:{self._name}, " \
               f"surname:{self._surname}"

    def __show_teachers(self):
        pass

    def show_menu(self):
        print(menu)
        choice = input()
        self.identifier[int(choice) - 1]




