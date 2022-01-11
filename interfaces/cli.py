from __future__ import annotations

import json
from typing import TYPE_CHECKING, Optional
import os

from data_model.group import Group
from data_model.student import Student
from data_model.subject import Subject
from datetime import date

if TYPE_CHECKING:
    from adapters.file_source import FileSource
# Уровни допуска-
# 0- учащийся
# 1- преподаватель
# 2- администратор
# Панели интерфейса
# 0- Общая после входа
# 1- Панель действий ученика
# 2- Панель действий учителя
# 3- Панель действий администратора
# Для возврата на предыдущую панель используем команду back
from data_model.teacher import Teacher


class CLI:
    def __init__(self, db_source: FileSource):
        self.data_of_panel = ["               Доступные действия:\n"
                              "   возможные действия       завершить сессию\n"
                              "                     \     /\n"
                              "                      1   2\n",

                              "               Доступные действия:\n"
                              "           мои группы       моё расписание\n"
                              "                     \     /\n"
                              "                      1   2\n"
                              "                           3 - изменить пароль\n",

                              "               Доступные действия:\n"
                              "     добавить ученика       изменить пароль\n"
                              "         в группу    \     /\n"
                              "                      1   2\n"
                              "                           3 -показать всех учеников\n"
                              "                      5   4         по группам\n"
                              "                     /     \ \n"
                              "        добавить урок       моё расписание\n",

                              "               Доступные действия:\n"
                              "        показать всех       изменить пароль\n"
                              "       пользователей \     /\n"
                              "                      1   2\n"
                              ]
        entrance = False
        self.__db_source = db_source
        inf = {}

        while entrance is False:
            print("Введите логин")
            login = input()  # Собираем с пользователя его данные, чтобы узнать, кто он
            print("Введите пароль")
            password = input()
            with open("logins_and_passwords.json") as file:
                data = file.read()
                read_data = json.loads(data)
                for i in read_data:
                    if i["login"] == login and i["password"] == password:
                        entrance = True
                        self.__status = i["status"]
                        inf = i
                        break
        if self.__status == 0:
            self.__user = Student.get_by_id(inf['object_id'], self.__db_source)
        else:
            self.__user = Teacher.get_by_id(inf['object_id'], self.__db_source)

        self.__timetable = f'Мое расписание на {date.today()}'

    def __get_my_timetable(self):
        if date.today().weekday() < 5:
            print(self.__timetable)

    def __get_all_group(self):
        if self.__status == 0:
            print('\n'.join([f'Группа {i.get_letter()}' for i in self.__user.get_all_groups()]))

    def __get_all_student(self):
        lst = {}
        groups = {}
        for i in Group.get_all(self.__db_source):
            if i.get_teacher_id() == self.__user.get_main_id():
                groups[i.get_letter()] = i
            print('Группа', i.get_letter())
            for j in i.get_all_students():
                lst[j.get_full_name()] = j
                print(j.get_full_name, end=', ')
            print('\n')
        return lst, groups

    def __new_group_for_student(self):
        if self.__status == 1:
            print('Выберите ученика из списка')
            lst, groups = self.__get_all_student()
            student_name = self.__input_processing(lst)
            print("Выберите группу из списка")
            group = groups[self.__input_processing(groups)]
            group.append_student(lst[student_name])

    def __new_subject_for_teacher(self):
        if self.__status == 1:
            print('Выберите предмет из списка')
            lst = {}
            for i in Subject.get_all(self.__db_source):
                lst[i.get_subject_name()] = i
                print(i.get_subject_name(), end=', ')
            print('\n')
            subject_name = self.__input_processing(lst)
            self.__user.append_subject(lst[subject_name])

    def __get_all_subjects(self):
        if self.__status == 1:
            print('\n'.join([f'Предмет {i.get_subject_name()}' for i in self.__user.get_subjects()]))

    def __input_processing(self, lst: Optional[list, dict]) -> str:
        user_answer = input()
        while user_answer not in lst:
            print('Введите еще раз')
            user_answer = input()
        return user_answer

    def show_menu(self, num_of_panel, right_answer=None):
        if right_answer is None:
            right_answer = ["back"]
        print(self.data_of_panel[num_of_panel])
        # Необходимо преорбазовать отбор ввода в отдельную функцию(принимаем на ввод корректные значения,
        # ругаем пользователя, пока он не введет одно из них)
        ans = input()
        while ans not in right_answer:
            ans = input()
        return ans

    def run(self):
        print("                Добро пожаловать!")
        input("                 Нажмите Enter,\n"
              "                чтобы продолжить")
        while True:
            os.system("cls")
            user_input = self.show_menu(num_of_panel=0, right_answer=["1", "2", "back"])
            if user_input == "1":
                if self.__status == 0:
                    user_input = self.show_menu(num_of_panel=1, right_answer=["1", "2", "3", "back"])
                    if user_input == "1":
                        self.__get_all_group()
                    elif user_input == "2":
                        self.__get_my_timetable()
                    elif user_input == "3":
                        pass
                    else:
                        pass
                elif self.__status == 1:
                    user_input = self.show_menu(num_of_panel=2, right_answer=["1", "2", "3", "4", "5", "back"])
                    if user_input == "1":
                        self.__get_all_group()
                    elif user_input == "2":
                        pass
                    elif user_input == "3":
                        self.__get_all_student()
                    elif user_input == "4":
                        self.__get_my_timetable()
                    elif user_input == "5":
                        self.__new_subject_for_teacher()
                    else:
                        pass
                elif self.__status == 2:
                    user_input = self.show_menu(num_of_panel=3, right_answer=["1", "2", "back"])
                    if user_input == "1":
                        self.__new_group_for_student()
                    elif user_input == "2":
                        pass
                    else:
                        pass
            else:
                break
