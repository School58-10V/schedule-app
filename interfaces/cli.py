import json
# Уровни допуска-
# 0- учащийся
# 1- преподаватель
# 2- администратор


class CLI:
    def __init__(self):
        login = input()  # Собираем с пользователя его данные, чтобы узнать, кто он
        password = input()
        entrance = False
        while entrance is False:
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
