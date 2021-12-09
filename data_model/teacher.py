from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from data_model.lesson_row import LessonRow
from data_model.lesson_rows_for_teachers import LessonRowsForTeachers
from data_model.parsed_data import ParsedData
import json

from data_model.abstract_model import AbstractModel
from typing import Optional, List, TYPE_CHECKING

from data_model.teachers_for_lesson_rows import TeachersForLessonRows

if TYPE_CHECKING:
    from adapters.file_source import FileSource


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

    def __init__(self, db_source: FileSource, fio: str, subject: str, object_id: Optional[int] = None,
                 office_id: int = None, bio: str = None,
                 contacts: str = None):
        super().__init__(db_source)
        self.__fio = fio
        self._object_id = object_id
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
                    # внимание! здесь может быть баг, т.к. порядок аргументов здесь
                    # не такой же как в __init__(), но я не уверен.
                    fio = i[0]
                    bio = i[1]
                    contacts = i[2]
                    office_id = int(i[3])
                    subject = i[4]

                    res.append(ParsedData(None, Teacher(fio=fio, subject=subject,
                                                        office_id=office_id, bio=bio,
                                                        contacts=contacts, object_id=None)))
                except IndexError as e:
                    exception_text = f"Строка {lines.index(i) + 1} не добавилась в [res]"
                    print(exception_text)
                    print(e)
                    res.append(ParsedData(exception_text, None))
                except Exception as e:
                    exception_text = f"Неизвестная ошибка в Teacher.parse():\n{e}"
                    print(exception_text)
                    res.append(ParsedData(exception_text, None))
        return res

    def __dict__(self) -> dict:
        return {"fio": self.__fio,
                "object_id": self._object_id,
                "bio": self.__bio,
                "contacts": self.__contacts,
                "office_id": self.__office_id,
                "subject": self.__subject}

    def __str__(self):
        return f'Teacher(fio = {self.__fio}, subject = {self.__subject}, bio = {self.__bio}, ' \
               f'contacts = {self.__contacts}) '

    def get_lesson_rows(self) -> List[LessonRow]:
        """
            Возвращает список словарей объектов TeacherForLessonRows используя db_source данный в __init__()
            :return: список словарей объектов TeacherForLessonRows
        """
        return LessonRowsForTeachers.get_lesson_rows_by_teacher_id(self._object_id, self._db_source)
