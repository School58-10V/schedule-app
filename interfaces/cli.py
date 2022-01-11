import json
from typing import TYPE_CHECKING, Optional

from data_model.group import Group
from data_model.student import Student
from data_model.subject import Subject

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
                              "                      1   2\n"
                              "                           3 - изменить пароль\n",

                              "               Доступные действия:\n"
                              "           мои группы       моё расписание\n"
                              "                     \     /\n"
                              "                      1   2\n",

                              "               Доступные действия:\n"
                              "     добавить ученика       изменить пароль\n"
                              "         в группу    \     /\n"
                              "                      6   1\n"
                              "показать все группы- 5     2 - показать всех учеников\n"
                              "      ученика         4   3            в группе\n"
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
            login = input()  # Собираем с пользователя его данные, чтобы узнать, кто он
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

    def __get_all_group(self):
        if self.__status == 0:
            print('\n'.join([f'Группа {i.get_letter()}' for i in self.__user.get_all_groups()]))

    def __new_group_for_student(self):
        if self.__status == 1:
            print('Выберите ученика из списка')
            spisok = {}
            groups = {}
            for i in Group.get_all(self.__db_source):
                if i.get_teacher_id() == self.__user.get_main_id():
                    groups[i.get_letter()] = i
                print('Группа', i.get_letter())
                for j in i.get_all_students():
                    spisok[j.get_full_name()] = j
                    print(j.get_full_name, end=', ')
                print('\n')
            student_name = self.__input_processing(spisok)
            print("Выберите группу из списка")
            group = groups[self.__input_processing(groups)]
            group.append_student(spisok[student_name])

    def __new_subject_for_teacher(self):
        if self.__status == 1:
            print('Выберите предмет из списка')
            spisok = {}
            groups = {}
            for i in Subject.get_all(self.__db_source):
                spisok[i.get_subject_name()] = i
                print(i.get_subject_name(), end=', ')
            print('\n')
            subject_name = self.__input_processing(spisok)
            self.__user.append_subject(spisok[subject_name])

    # Не успела доделать
    # def __parse_new_group(self, file_location):
    #     if self.__status == 0:
    #         groups = Group.parse(file_location, self.__db_source)

    def __get_all_subjects(self):
        if self.__status == 1:
            print('\n'.join([f'Предмет {i.get_subject_name()}' for i in self.__user.get_subjects()]))

    # def __get_timetable(self):
    #     if self.__status == 0:
    #         for i in self.__user.get_all_groups():
    #
    #         self.__user.

    def __input_processing(self, spisok: Optional[list, dict]) -> str:
        user_answer = input()
        while user_answer not in spisok:
            print('Введите еще раз')
            user_answer = input()
        return user_answer

    def show_menu(self, num_of_panel, right_answer=["back"]):
        print(self.data_of_panel[num_of_panel])
        # Необходимо преорбазовать отбор ввода в отдельную функцию(принимаем на ввод корректные значения,
        # ругаем пользователя, пока он не введет одно из них)
        ans = input()
        while ans not in right_answer:
            ans = input()
        return ans
