import json


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
                        status = i["status"]
