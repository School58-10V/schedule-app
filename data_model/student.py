from datetime import date
from typing import Optional


class Student:
    """
        Класс ученика.
    """

    def __init__(
            self, full_name: str, date_of_birth: date, student_id: Optional[int] = None,
            contacts: Optional[str] = None, bio: Optional[str] = None
    ):
        self.__full_name = full_name
        self.__date_of_birth = date_of_birth
        self.__student_id = student_id
        self.__contacts = contacts
        self.__bio = bio

    def get_full_name(self) -> str:
        return self.__full_name

    def get_date_of_birth(self) -> date:
        return self.__date_of_birth

    def get_id(self) -> Optional[int]:
        return self.__student_id

    def get_contacts(self) -> Optional[str]:
        return self.__contacts

    def get_bio(self) -> Optional[str]:
        return self.__bio
