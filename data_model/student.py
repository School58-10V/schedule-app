from datetime import date


class Student:
    """
        Класс ученика.
    """

    def __init__(
            self, full_name: str, date_of_birth: date, student_id: int = None,
            contacts: str = None, bio: str = None
    ):
        self.__full_name = full_name
        self.__date_of_birth = date_of_birth
        self.__student_id = student_id
        self.__contacts = contacts
        self.__bio = bio

    def get_full_name(self):
        return self.__full_name

    def get_date_of_birth(self):
        return self.__date_of_birth

    def get_id(self):
        return self.__student_id

    def get_contacts(self):
        return self.__contacts

    def get_bio(self):
        return self.__bio
