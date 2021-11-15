from __future__ import annotations  # нужно чтобы parse мог быть типизирован
from data_model.abstract_model import AbstractModel
from typing import Optional, List


class Teacher(AbstractModel):
    """
        Класс учителя.
        fio - ФИО
        object_id - ид учителя
        bio - инфа о учителе
        contacts - Контакты учителя
        office_id - закреплённый кабинет
        subject - его предмет.
    """
    def __init__(self, fio: str, object_id: int, subject: str, office_id: int = None, bio: str = None,
                 contacts: str = None):
        self.__fio = fio
        self.__object_id = object_id
        self.__bio = bio
        self.__contacts = contacts
        self.__office_id = office_id
        self.__subject = subject

    def get_fio(self) -> str:
        return self.__fio

    def get_bio(self) -> Optional[str]:
        return self.__bio

    def get_contacts(self) -> Optional[str]:
        return self.__contacts

    def get_subject(self) -> str:
        return self.__subject

    def get_office_id(self) -> Optional[int]:
        return self.__office_id

    @staticmethod
    def parse(file_location) -> List[(Optional[str], Optional[Teacher])]:
        with open(file_location, encoding='utf-8') as f:
            lines = [i.split(';') for i in f.read().split('\n')[1:]]
            res = []

            for i in lines:
                try:
                    fio = i[0]
                    subject = i[1]
                    office_id = i[2]
                    bio = i[3]
                    contacts = i[4]

                    res.append((None, Teacher(fio, subject, office_id, bio, contacts)))
                except IndexError as e:
                    exception_text = f"Строка {lines.index(i) + 1} не добавилась в [res]"
                    print(exception_text)
                    print(e)
                    res.append((exception_text, None))
                except Exception as e:
                    exception_text = f"Неизвестная ошибка в Teacher.parse():\n{e}"
                    print(exception_text)
                    res.append((exception_text, None))
        return res

    def __dict__(self) -> dict:
        return {"fio": self.__fio,
                "object_id": self.__object_id,
                "bio": self.__bio,
                "contacts": self.__contacts,
                "office_id": self.__office_id,
                "subject": self.__subject}

    def __str__(self):
        return f'Teacher(fio = {self.__fio}, subject = {self.__subject}, bio = {self.__bio}, ' \
               f'contacts =  {self.__contacts}) '
