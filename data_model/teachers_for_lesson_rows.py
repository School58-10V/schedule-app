from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from data_model.abstract_model import AbstractModel
from data_model.parsed_data import ParsedData

if TYPE_CHECKING:
    from adapters.file_source import FileSource
    from data_model.teacher import Teacher


class TeachersForLessonRows(AbstractModel):
    """
        Класс учителя в LessonRow. Используется для m2m отношения между
        Teacher и LessonRow
        teacher_id - Идентификационный номер учителя
        lesson_row_id - Идентификационный номер ряда уроков
        object_id - Идентификационный номер учителя на ряд уроков
    """

    def __init__(self, db_source: FileSource, teacher_id: int, lesson_row_id: int, object_id: Optional[int] = None):
        super().__init__(db_source)
        self.__teacher_id = teacher_id
        self.__lesson_row_id = lesson_row_id
        self._object_id = object_id

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_lesson_row_id(self) -> int:
        return self.__lesson_row_id

    def __str__(self) -> str:
        return f'TeachersForLessonRows(teacher_id: {self.get_teacher_id()},' \
               f' lesson_row_id: {self.get_lesson_row_id()},' \
               f' object_id: {self.get_main_id()})'

    def __dict__(self) -> dict:
        return {"teacher_id": self.get_teacher_id(),
                "lesson_row_id": self.get_lesson_row_id(),
                "object_id": self.get_main_id()}

    # @staticmethod
    # def parse(file_location: str, db_source: FileSource) -> List[(Optional[str], Optional[TeachersForLessonRows])]:
    #     file = open(file_location, 'r', encoding='utf-8')
    #     lines = file.read().split('\n')[1:]
    #     file.close()
    #     res = []
    #     for i in lines:
    #         j = i.split(';')
    #         try:
    #             teacher_id = int(j[0])
    #             lesson_row_id = int(j[1])
    #
    #             res.append(ParsedData(None, TeachersForLessonRows(db_source=db_source,
    #                                                               teacher_id=teacher_id,
    #                                                               lesson_row_id=lesson_row_id)))
    #         except (IndexError, ValueError) as error:
    #             exception_text = f"Запись {lines.index(i) + 1} строка {lines.index(i) + 2} " \
    #                              f"не добавилась в [res].\nОшибка: {error}"
    #             res.append(ParsedData(exception_text, None))
    #         except Exception as error:
    #             exception_text = f"Неизвестная ошибка в TeachersForLessonRows.parse():\n{error}"
    #             print(exception_text + '\n')
    #             res.append(ParsedData(exception_text, None))
    #     return res

    @classmethod
    def _get_collection_name(cls):
        return 'LessonRowsAndTeachers'

    @classmethod
    def get_teachers_by_lesson_row_id(cls, lesson_row_id: int, db_source: FileSource) -> List[Teacher]:
        """
        возвращает всех учителей, у которых есть определенный lesson_row_id

        :param lesson_row_id: идшник LessonRow который должен быть у учителя
        :param db_source: наш дб сорс
        :return: список идшинков учителей, у которых lesson_row_id равен тому что мы передали
        """
        from data_model.teacher import Teacher
        return [
            Teacher.get_by_id(i['teacher_id'], db_source=db_source)
            for i in db_source.get_by_query(cls._get_collection_name(), {'lesson_row_id': lesson_row_id})
            ]

    @classmethod
    def get_lesson_rows_by_teacher_id(cls, teacher_id: int, db_source: FileSource) -> List[LessonRow]:
        """
        возвращает всех учителей, у которых есть определенный teacher_id

        :param teacher_id: идшник Teacher который должен быть у учителя
        :param db_source: наш дб сорс
        :return: список идшинков учителей, у которых teacher_id равен тому что мы передали
        """
        from data_model.lesson_row import LessonRow

        return [
            LessonRow.get_by_id(i['lesson_row_id'], db_source=db_source)
            for i in db_source.get_by_query(cls._get_collection_name(), {'teacher_id': teacher_id})
        ]
