from __future__ import annotations  # нужно чтобы parse мог быть типизирован
import json

from typing import Optional, List


class StudentInGroup:
    """
        Класс ученика в группе. Используется для m2m отношения между
        Group и Student
        student_id - айди ученика
        group_id - айди группы
        student_group_id - айди группы учeников
    """

    def __init__(self, student_id: int, group_id: int, student_group_id: Optional[int] = None):
        self.__student_id = student_id
        self.__group_id = group_id
        self.__student_group_id = student_group_id

    def get_student_id(self) -> int:
        return self.__student_id

    def get_group_id(self) -> int:
        return self.__group_id

    def get_student_group_id(self) -> Optional[int]:
        return self.__student_group_id

    @staticmethod
    def parse(file_location) -> List[(Optional[str], Optional[StudentInGroup])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []

        for i in lines:
            try:
                student_id = int(i[0])
                group_id = int(i[1])
                student_group_id = int(i[2])
                res.append((None, StudentInGroup(student_id, group_id, student_group_id)))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 1} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append((exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в Student_in_group.parse():\n{e}"
                print(exception_text)
                res.append((exception_text, None))

        return res

    def __str__(self):
        return f''

    def __dict__(self) -> dict:
        return {'student_id': self.__student_id,
                'group_id': self.__group_id,
                'student_group_id': self.__student_group_id}

    def __serialize_to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

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
