# ------------------------
# [1] show_timetable
# ------------------------
# [2] show_teachers
# ------------------------
menu = [{}, {}]

class Cli:
    def __init__(self, user_status: str, class_of_user: str, name: str, surname: str):
        _user_status = user_status
        _class_of_user = class_of_user
        _name = name
        _surname = surname

    def __show_timetable(self):
        pass

    def __show_classes(self):
        pass

    @classmethod
    def __log_in(cls) -> str:
        pass

    def __show_teachers(self):
        pass

    @classmethod
    def __show_menu(cls):
        pass