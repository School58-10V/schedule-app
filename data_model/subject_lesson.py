from __future__ import annotations
import json
from typing import Optional, List


class Subject:
    """
              name - Название предмета
        subject_id - Идентификационный номер предмета

    """
    def __init__(self, name: str = None, subject_id: int = None):
        self.__subject_name = name
        self.__subject_id = subject_id

    def get_subject_id(self) -> int:
        return self.__subject_id

    def get_subject_name(self) -> str:
        return self.__subject_name

    @staticmethod
    def parse(file_location: str) -> List[(Optional[str], Optional[Subject])]:
        file = open(file_location, 'r', encoding='utf-8')
        lines = file.read().split('\n')[1:]
        file.close()
        # lines = [i.split(';') for i in lines] Зачем отдельно проходить циклом для split,
        # если можно сделать все в одном цикле?
        res = []
        for i in lines:
            j = i.split(';')
            try:
                name_subject = j[0]
                res.append((None, Subject(name=name_subject)))
            except IndexError as error:
                exception_text = f"Запись {lines.index(i) + 1} строка {lines.index(i) + 2} " \
                                 f"не добавилась в [res].\nОшибка: {error}"
                print(exception_text)
                res.append((exception_text, None))
            except Exception as error:
                exception_text = f"Неизвестная ошибка в Subject.parse():\n{error}"
                print(exception_text + '\n')
                res.append((exception_text, None))
        return res

    def __str__(self):
        return f'Subject(subject_name: {self.__subject_name})'

    def __dict__(self) -> dict:
        return {
            "subject_id": self.__subject_id,
            "subject_name": self.__subject_name
        }

    def serialize_to_json(self, indent: int = None) -> str:
        return json.dumps(self.__dict__(self), ensure_ascii=False, indent=indent)

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
        current_records.append(self.__dict__(self))
        target_json = self.__class__.serialize_records_to_json(current_records)
        with open(f"{output_path}/{type(self).__name__}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)
