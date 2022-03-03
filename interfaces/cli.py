from interfaces import teacher_interface
from interfaces.teacher_interface import TeachersInterface
# from interfaces import StudentsInterface
from adapters.db_source import DBSource


class Cli:
    def __init__(self, db_source: DBSource):
        self.__db_source = db_source
        self.__usr_interface = None

    def choose_usr_interface(self):
        print("Вы учитель или ученик? 0 если учитель, 1 если ученик")
        param = input()
        try:
            param = int(param)
        except (ValueError):
            print("Попробуйте снова!")
        if param == 0:
            self.__usr_interface = TeachersInterface(self.__db_source)
        elif param == 1:
            pass
            # self.__usr_interface = StudentsInterface