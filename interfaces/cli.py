import json
from typing import TYPE_CHECKING

from data_model.group import Group

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


class CLI:
    def __init__(self, db_source: FileSource):
        self.data_of_panel = ["               Доступные действия:\n"
                              "   возможные действия       завершить сессию\n"
                              "                     \     /\n"
                              "                      1   2\n",

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

        while entrance is False:
            login = input()  # Собираем с пользователя его данные, чтобы узнать, кто он
            password = input()
            with open("interfaces/logins_and_passwords.json") as file:
                data = file.read()
                read_data = json.loads(data)
                for i in read_data:
                    if i["login"] == login and i["password"] == password:
                        entrance = True
                        self.__status = i["status"]
                        break

    def __get_all_group(self):
        if self.__status == 0:
            print('\n'.join([f'Группа {i.get_letter()}' for i in self.__user.get_all_groups()]))

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

    def show_menu(self, num_of_panel):
        print(self.data_of_panel[num_of_panel])  # Что это?
        answer = False
        # Необходимо преорбазовать отбор ввода в отдельную функцию(принимаем на ввод корректные значения,
        # ругаем пользователя, пока он не введет одно из них)
        ans = ''
        while answer is False:
            ans = input()
            if ans in ["1", "2"]:
                answer = True
        if ans == "1":
            return 1
        if ans == "2":
            return 2
