from __future__ import annotations  # нужно чтобы parse мог быть типизирован
import json
from datetime import date

from typing import Optional, List

from data_model.abstract_model import AbstractModel


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
            self, full_name: str, date_of_birth: date, object_id: Optional[int] = None,
            contacts: Optional[str] = None, bio: Optional[str] = None
    ):
        self.__full_name = full_name
        self.__date_of_birth = date_of_birth
        self.__object_id = object_id
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

                    res.append(
                        (None, Student(full_name, date_of_birth, contacts, bio)))
                except IndexError as e:
                    exception_text = f"Строка {lines.index(i) + 1} не добавилась в [res]"
                    print(exception_text)
                    print(e)
                    res.append((exception_text, None))
                except Exception as e:
                    exception_text = f"Неизвестная ошибка в Student.parse():\n{e}"
                    print(exception_text)
                    res.append((exception_text, None))

        return res

    def __str__(self):
        return f'Student(full_name = {self.__full_name}, date_of_birth = {self.__date_of_birth}, contacts = {self.__contacts}, bio =  {self.__bio}) '

    def __dict__(self) -> dict:
        return {
            "full_name": self.__full_name,
            "date_of_birth": self.__date_of_birth,
            "object_id": self.__object_id,
            "contacts": self.__contacts,
            "bio": self.__bio
        }

    def serialize_to_json(self, indent: int = None) -> str:
        return json.dumps(self.__dict__(), ensure_ascii=False, indent=indent)

    @staticmethod
    def serialize_records_to_json(records: list, indent: int = None) -> str:
        return json.dumps(records, ensure_ascii=False, indent=indent)

    @classmethod
    def __read_json_db(cls, db_path) -> list:
        try:
            with open(f"{db_path}/{cls.__name__}.json",
                      mode="r", encoding='utf-8') as data_file:
                record = json.loads(data_file.read())
                return record
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []
