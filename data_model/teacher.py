from __future__ import annotations  # нужно чтобы parse мог быть типизирован
import json

from typing import Optional, List


class Teacher:
    """
        Класс учителя.
        fio - ФИО
        teacher_id - ид учителя
        bio - инфа о учителе
        contacts - Контакты учителя
        office_id - закреплённый кабинет
        subject - его предмет.
    """
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

                    res.append(
                        (None, Teacher(fio, subject, office_id, bio, contacts)))
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
                "teacher_id": self.__teacher_id,
                "bio": self.__bio,
                "contacts": self.__contacts,
                "office_id": self.__office_id,
                "subject": self.__subject}

    def __str__(self):
        return f'Teacher(fio = {self.__fio}, subject = {self.__subject}, bio = {self.__bio}, ' \
               f'contacts =  {self.__contacts}) '

    def serialize_to_json(self):
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

    def save(self, output_path: str = './db'):
        current_records = self.__read_json_db(output_path)
        current_records.append(self.__dict__())
        target_json = self.__class__.serialize_records_to_json(current_records)
        with open(f"{output_path}/{type(self).__name__}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)

    @classmethod
    def get_all(cls, db_path: str = "./db") -> list[Teacher]:
        return [cls(**i) for i in cls.__read_json_db(db_path)]

    @classmethod
    def get_by_id(cls, teacherId: int, db_path: str = "./db") -> Teacher:
        for i in cls.__read_json_db(db_path):
            if int(teacher_id) == teacherId:
                return Teacher(**i)
        return ValueError(f"Объект с id {teacherId} не найден")
