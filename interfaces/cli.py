import json


class CLI:
    def __init__(self):
        login = input()
        password = input()
        entrance = False
        while entrance is False:
            with open("interfaces/logins_and_passwords.json") as data:
                read_data = json.load(data)
                for i in read_data:
                    if i["login"] == login and i["password"] == password:
                        entrance = True
                        status = i["status"]
