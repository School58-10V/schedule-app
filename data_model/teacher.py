from __future__ import annotations

import json

from typing import Optional, List


# fio - ФИО, что впринципе логично
# teacher_id - ид учителя
# bio - инфа о учителе
# contacts - Контакты учителя
# office_id - закреплённый кабинет
# lesson - сделайте m2m связь, т.к. не знаю, не умею

class Teacher:
    def __init__(self, fio: str, teacher_id: int, subject: str, office_id: int = None, bio: str = None,
                 contacts: str = None):
        self.__fio = fio
        self.__teacher_id = teacher_id
        self.__bio = bio
        self.__contacts = contacts
        self.__office_id = office_id
        self.__subject = subject

    def get_fio(self) -> str:
        return self.__fio

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_subject(self) -> str:
        return self.__subject

    def get_office_id(self) -> Optional[int]:
        return self.__office_id

    def get_bio(self) -> Optional[str]:
        return self.__bio

    def get_contacts(self) -> Optional[str]:
        return self.__contacts

    def __serialize_to_json(self):
        return json.dumps({"fio": self.__fio,
                           "teacher_id": self.__teacher_id,
                           "bio": self.__bio,
                           "contacts": self.__contacts,
                           "subject": self.__subject,
                           "office_id": self.__office_id}, ensure_ascii=False)

    def save(self, path="./db/teacher.json"):
        with open(path, mode="w", encoding='utf-8') as data_file:
            data_file.write(self.__serialize_to_json())

    def __str__(self):
        return f'Teacher(fio={self.__fio}, teacher_id={self.__teacher_id}, ' \
               f'bio={self.__bio}, contacts={self.__contacts}), subject={self.__subject}), office_id={self.__office_id})'

    @staticmethod
    def parse(file_location) -> List[(Optional[str], Optional[Teacher])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []
        for i in lines:
            try:
                fio = i[0]
                teacher_id = i[1]
                subject = i[2]
                office_id = i[3]
                bio = i[4]
                contacts = i[5]

                res.append((None, Teacher(fio, int(teacher_id), subject, int(office_id), bio, contacts)))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append((exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в Teacher.parse():\n{e}"
                print(exception_text)
                res.append((exception_text, None))
        return res
