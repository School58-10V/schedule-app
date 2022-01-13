class User:
    def __init__(self):
        self.__access_level = ""
        self.__logged_in = True
        self.__name = ""
        self.__surname = ""
        self.__class_of_user = ""

    def get_user_state(self) -> str:
        return self.__logged_in

    def get_identity(self) -> list:
        return [self.__name, self.__surname]

    def get_access_level(self) -> str:
        return self.__access_level

    def get_class_of_user(self) -> str:
        return self.__class_of_user

    def log_in(self, name: str, surname: str, access_level: str = "Студент", uclass: str = ""):
        self.__name, self.__surname, self.__access_level = name.lower(), surname.lower(), access_level.lower()
        if self.__access_level == "студент":
            self.__class_of_user = uclass
        self.__logged_in = True
        print("Вход проведён успешно!")
