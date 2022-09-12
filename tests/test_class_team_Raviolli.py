from __future__ import annotations

import random
import datetime

from typing import TYPE_CHECKING, List, Dict
from data_model.group import Group
from data_model.lesson_row import LessonRow
from data_model.subject import Subject
from data_model.teacher import Teacher
from data_model.timetable import TimeTable

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
        subjects = Subject.get_all(db_source=self.get_db_source())
        if len(subjects) == 0:
            raise ValueError("У нас нет никаких предметов :0")
        return subjects

    def __get_group(self, class_letter: str, grade: int) -> Group:
        """
        Возвращает группу по букве и классу
        :param class_letter: Буква класса
        :param grade: Класс (номер, год обучения)
        :return:
        """
        groups = Group.get_by_class_letters(db_source=self.get_db_source(), class_letter=class_letter, grade=grade)

        if len(groups) == 1:
            return groups[0]
        raise ValueError("Ошибка в базе данных!!! Групп с таким названием несколько!")

    def __get_all_teachers(self) -> List:
        """
        Возвращает всех учителей
        :return:
        """
        teachers = Teacher.get_all(db_source=self.get_db_source())
        if len(teachers) == 0:
            raise ValueError("У нас нет учителей :0")
        return teachers

    @staticmethod
    def __get_year() -> int:
        """
        Возвращает текущий год
        :return:
        """
        return datetime.date.today().year

    def run(self, lst: list, class_letter: str, grade: int) -> Dict:
        """
        Главный метод, запускающий все
        :param lst: список с количеством пар на дни
        :param class_letter: буква класса
        :param grade: год обучения
        :return:
        """
        group = self.__get_group(class_letter=class_letter, grade=grade)
        subjects = self.__get_all_subject()
        teachers = self.__get_all_teachers()
        timetable = TimeTable.get_by_year(year=self.__get_year(), db_source=self.get_db_source())
        counter = 0
        lesson_rows = {}
        for i in random.sample(range(5), 3):
            start_time = 540
            end_time = 585
            lesson_rows[i] = []
            for j in range(lst[counter]):
                subject = random.choice(subjects)
                try:
                    teacher = random.choice(subject.get_teachers())
                except IndexError:
                    teacher = random.choice(teachers)
                    subject.append_teacher(teacher)
                office_id = teacher.get_office_id()
                lesson_row = LessonRow(db_source=self.get_db_source(),
                                       day_of_the_week=i,
                                       group_id=group.get_main_id(),
                                       end_time=end_time,
                                       start_time=start_time,
                                       room_id=office_id,
                                       subject_id=subject.get_main_id(),
                                       timetable_id=timetable.get_main_id()).save()
                lesson_rows[i].append(lesson_row)
            counter += 1
            start_time += 60
            end_time += 60
        return lesson_rows
