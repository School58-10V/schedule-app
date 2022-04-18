from data_model.student import Student
from data_model.teacher import Teacher
from interfaces.teacher_interface import TeacherInterface
from interfaces.student_interface import StudentInterface
from adapters.db_source import DBSource
from flask import Flask, request

app = Flask(__name__)

class Cli:
    def __init__(self):
        self.__db_source = DBSource()

    def run(self):
        user_interface = None
        name = input('Ваше ФИО: ')
        teacher_list = Teacher.get_by_name(name, self.__db_source)
        student_list = Student.get_by_name(name, self.__db_source)

        if len(teacher_list) + len(student_list) > 1:
            # просим выбрать какой он именно из списка
            counter = 0
            people_list = [(i.get_fio(), i.get_main_id(), 'teacher') for i in teacher_list] + \
                          [(i.get_fio(), i.get_main_id(), 'student') for i in student_list]
            a = input('Выберите себя из списка: ')
            # TODO: доделать

        elif len(teacher_list) + len(student_list) == 0:
            print('Не нашел никого с таким именем!')
            if len(teacher_list) == 1:
                pass
        else:
            if len(teacher_list) == 1:
                user_interface = StudentInterface(self.__db_source, teacher_list[0].get_main_id())
            else:
                user_interface = TeacherInterface(self.__db_source, student_list[0].get_main_id())
