from __future__ import annotations
from typing import Optional, List
from data_model.abstract_model import AbstractModel


class Subject(AbstractModel):
    """
              name - Название предмета
        object_id - Идентификационный номер предмета
    """

    def __init__(self, subject_name: Optional[str] = None,
                 object_id: Optional[int] = None):
        self.__subject_name = subject_name
        self.__object_id = object_id

    def get_subject_name(self) -> str:
        return self.__subject_name

    @staticmethod
    def parse(file_location: str) -> List[(Optional[str], Optional[Subject])]:
        file = open(file_location, 'r', encoding='utf-8')
        lines = file.read().split('\n')[1:]
        file.close()
        res = []
        for i in lines:
            j = i.split(';')
            try:
                name_subject = j[0]
                res.append((None, Subject(subject_name=name_subject)))
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
        return {"object_id": self.__object_id,
                "subject_name": self.__subject_name}
