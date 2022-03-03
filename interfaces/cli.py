from interfaces import teacher_interface
from interfaces.teacher_interface import TeacherInterface
from interfaces import student_interface
from interfaces.student_interface import StudentInterface
from adapters.db_source import DBSource


class Cli:
    def __init__(self, db_source: DBSource, usr_id: int):
        self.__db_source = db_source
        self.__usr_interface = None
        self.__usr_id = usr_id

    def choose_usr_interface(self):
        print("Вы учитель или ученик? 0 если учитель, 1 если ученик")
        param = input()
        try:
            param = int(param)
        except ValueError:
            print("Попробуйте снова!")
        if param == 0:
            self.__usr_interface = TeacherInterface(self.__db_source, self.__usr_id)
        elif param == 1:
            self.__usr_interface = StudentInterface(self.__db_source, self.__usr_id)