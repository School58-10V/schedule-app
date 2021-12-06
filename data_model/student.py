from __future__ import annotations  # нужно чтобы parse мог быть типизирован
from datetime import date
from data_model.parsed_data import ParsedData
from typing import Optional, List, TYPE_CHECKING

from data_model.abstract_model import AbstractModel
from data_model.student_in_group import StudentInGroup

if TYPE_CHECKING:
    from adapters.file_source import FileSource


class Student(AbstractModel):
    """
        Класс ученика.
        full name - полное имя студента
        date_of_birth - дата рождения ученика
        object_id - id студента
        contacts - контакты родителей ученика
        bio - биография студента
    """

    def __init__(
            self, db_source: FileSource, full_name: str, date_of_birth: date, object_id: Optional[int] = None,
            contacts: Optional[str] = None, bio: Optional[str] = None
            ):
        super().__init__(db_source)
        self.__full_name = full_name
        self.__date_of_birth = date_of_birth
        self._object_id = object_id
        self.__contacts = contacts
        self.__bio = bio

    def get_full_name(self) -> str:
        return self.__full_name

    def get_date_of_birth(self) -> date:
        return self.__date_of_birth

    def get_contacts(self) -> Optional[str]:
        return self.__contacts

    def get_bio(self) -> Optional[str]:
        return self.__bio

    @staticmethod
    def parse(file_location) -> List[(Optional[str], Optional[Student])]:
        with open(file_location, encoding='utf-8') as f:
            lines = [i.split(';') for i in f.read().split('\n')[1:]]
            res = []

            for i in lines:
                try:
                    full_name = i[0]
                    date_of_birth = date(i[1])
                    contacts = str(i[2])
                    bio = i[3]

                    res.append(ParsedData(None, Student(full_name, date_of_birth, contacts, bio)))
                except IndexError as e:
                    exception_text = f"Строка {lines.index(i) + 1} не добавилась в [res]"
                    print(exception_text)
                    print(e)
                    res.append(ParsedData(exception_text, None))
                except Exception as e:
                    exception_text = f"Неизвестная ошибка в Student.parse():\n{e}"
                    print(exception_text)
                    res.append(ParsedData(exception_text, None))

        return res

    def __str__(self):
        return f'Student(full_name = {self.__full_name}, date_of_birth = {self.__date_of_birth}, contacts = {self.__contacts}, bio =  {self.__bio}) '

    def __dict__(self) -> dict:
        return {
            "full_name": self.__full_name,
            "date_of_birth": self.__date_of_birth,
            "object_id": self._object_id,
            "contacts": self.__contacts,
            "bio": self.__bio
            }

    def get_all_student_group(self) -> list:
        # Берем все
        all_student_group = StudentInGroup.get_all(db_source=self._db_source)
        # Проходимся по списку циклом, проверяя равен ли id
        # студента с id данного студента и, если да, добавляем
        # его в список, который потом возвращаем
        return [i.get_group_id() for i in all_student_group if i.get_student_id() == self._object_id]
