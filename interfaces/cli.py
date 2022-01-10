class CLI:
    def __init__(self):
        login = input()
        password = input()
        entrance = False
        while entrance is False:
            with open("interfaces/logins_and_passwords.json") as data:
                for i in data:
                    if data[i]["login"] == login and login[i]["password"] == password:
                        entrance = True
                        status = data[i]["status"]
