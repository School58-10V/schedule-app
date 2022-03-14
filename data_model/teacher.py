from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from adapters.abstract_source import AbstractSource
from data_model.lesson_row import LessonRow
from data_model.parsed_data import ParsedData

from data_model.abstract_model import AbstractModel
from typing import Optional, List, TYPE_CHECKING

from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from data_model.teachers_for_subjects import TeachersForSubjects
from adapters.db_source import DBSource

if TYPE_CHECKING:
    from adapters.db_source import DBSource
    from data_model.subject import Subject


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

    def __init__(self, db_source: DBSource, fio: str, object_id: Optional[int] = None,
                 office_id: int = None, bio: str = None,
                 contacts: str = None):
        super().__init__(db_source)
        self.__fio = fio
        self._object_id = object_id
        self.__bio = bio
        self.__contacts = contacts
        self.__office_id = office_id

    def get_fio(self) -> str:
        return self.__fio

    def get_bio(self) -> Optional[str]:
        return self.__bio

    def get_contacts(self) -> Optional[str]:
        return self.__contacts

    def get_office_id(self) -> Optional[int]:
        return self.__office_id

    @staticmethod
    def parse(file_location: str, db_source: DBSource) -> List[(Optional[str], Optional[Teacher])]:
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

                    res.append(ParsedData(None, Teacher(db_source=db_source, fio=fio,
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

    def get_lesson_rows(self) -> List[LessonRow]:
        """
            Возвращает список объектов LessonRow используя db_source данный в __init__()
            :return: список объектов LessonRow
        """
        return TeachersForLessonRows.get_lesson_rows_by_teacher_id(self.get_main_id(), self.get_db_source())

    def get_subjects(self) -> List[Subject]:
        """
            Возвращает список объектов Subject используя db_source данный в __init__()
            :return: список объектов Subject
        """
        return TeachersForSubjects.get_subjects_by_teacher_id(self.get_main_id(), self.get_db_source())

    def append_lesson_row(self, lesson_row_obj: LessonRow) -> Teacher:
        """
        Создает сущность TeachersForLessonRows
        :param lesson_row_obj: LessonRow связь с которым мы хотим создать
        :return:
        """
        obj = TeachersForLessonRows(self.get_db_source(), lesson_row_id=lesson_row_obj.get_main_id(),
                                    teacher_id=self.get_main_id())
        for i in self.get_lesson_rows():
            if obj.get_lesson_row_id() == i.get_main_id():
                return self
        obj.save()
        return self

    def append_subject(self, subject_obj: Subject) -> Teacher:
        """
        Создает сущность TeachersForSubjects
        :param subject_obj: Subject связь с которым мы хотим удалить
        :return: сущность Teacher над которой работаем
        """
        obj = TeachersForSubjects(
            self.get_db_source(), subject_id=subject_obj.get_main_id(),
            teacher_id=self.get_main_id()
        )
        for i in self.get_subjects():
            if obj.get_subject_id() == i.get_main_id():
                return self
        obj.save()
        return self

    def remove_lesson_row(self, lesson_row_obj: LessonRow) -> Teacher:
        """
        Удаляет сущность TeachersForLessonRow, которая обозначает связь этого Teacher и lesson_row_obj
        :param lesson_row_obj: LessonRow связь с которым мы хотим удалить
        :return: сущность Teacher над которой работаем
        """
        for i in TeachersForLessonRows.get_by_lesson_row_and_teacher_id(lesson_row_obj.get_main_id(), self.get_main_id(), self.get_db_source()):
            i.delete()
        return self

    def remove_subject(self, subject_obj: Subject) -> Teacher:
        """
        Удаляет сущность TeachersForSubjects, которая обозначает связь этого Teacher и subject_obj
        :param subject_obj: Subject связь с которым мы хотим удалить
        :return: сущность Teacher над которой работаем
        """
        for i in TeachersForSubjects.get_by_subject_and_teacher_id(subject_obj.get_main_id(), self.get_main_id(), self.get_db_source()):
            i.delete()
        return self

    @classmethod
    def get_by_name(cls, name: str, source: AbstractSource) -> List[Teacher]:
        return [Teacher(**i) for i in source.get_by_query(cls._get_collection_name(), {'fio': name})]

    def __dict__(self) -> dict:
        return {"fio": self.get_fio(),
                "object_id": self.get_main_id(),
                "bio": self.get_bio(),
                "contacts": self.get_contacts(),
                "office_id": self.get_office_id()}

    def __str__(self):
        return f'Teacher(fio = {self.get_fio()}, bio = {self.get_bio()}, ' \
               f'contacts = {self.get_contacts()}) '
