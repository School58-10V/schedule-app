from __future__ import annotations
from typing import TYPE_CHECKING, List
from data_model.group import Group
from data_model.subject import Subject

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class TestClass:
    def __init__(self, db_source: DBSource):
        self.__db_source = db_source

    def get_db_source(self) -> DBSource:
        """
        Возвращает адаптер для базу данных
        :return: DBSource
        """
        return self.__db_source

    def __get_all_subject(self) -> List:
        """
        Возвращает список всех предметов
        :return:
        """
        return Subject.get_all(db_source=self.get_db_source())

    def __get_group(self, class_letter: str, grade: int) -> Group:
        """
        Возвращает группу по букве и классу
        :param class_letter: Буква класса
        :param grade: Класс (номер, год)
        :return:
        """
        groups = Group.get_by_class_letter(db_source=self.get_db_source(), class_letter=class_letter, grade=grade)
        if len(groups) != 1:
            return groups[0]
        raise ValueError("Ошибка в базе данных!!! Групп с таким названием несколько!")



    def run(self, num1: int, num2: int, num3: int, class_letter: str, grade: int):
        """
        Главный метод, запускающий все
        :param num1:
        :param num2:
        :param num3:
        :param class_letter:
        :param grade:
        :return:
        """
        group = self.__get_group(class_letter=class_letter, grade=grade)

        pass
