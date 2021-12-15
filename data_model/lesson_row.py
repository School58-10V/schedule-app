from __future__ import annotations
from data_model.abstract_model import AbstractModel
from typing import Optional, List, TYPE_CHECKING
from data_model.parsed_data import ParsedData
from data_model.teachers_for_lesson_rows import TeachersForLessonRows

if TYPE_CHECKING:
    from data_model.teacher import Teacher
    from adapters.file_source import FileSource


class LessonRow(AbstractModel):
    def __init__(self, db_source: FileSource, count_studying_hours: int, group_id: int, subject_id: int, room_id: int,
                 start_time: int, end_time: int, timetable_id: int, object_id: Optional[int] = None):
        # TODO: write down
        """
            :param count_studying_hours: ????
            :param db_source: Адаптер бд сорса
            :param start_time:  начальное время
            :param end_time: конечное время
            :param group_id: номер группы
            :param subject_id: айди предмета
            :param room_id: айди комнаты
            :param timetable_id: год в который происходят уроки
            :param object_id: айди самого класса ряд уроков
        """
        super().__init__(db_source)
        self.__count_studying_hours = count_studying_hours
        self.__start_time = start_time
        self.__end_time = end_time
        self.__group_id = group_id
        self.__subject_id = subject_id
        self.__room_id = room_id
        self.__timetable_id = timetable_id
        self._object_id = object_id

    def get_count_studying_hours(self) -> int:
        return self.__count_studying_hours

    def get_group_id(self) -> int:
        return self.__group_id

    def get_subject_id(self) -> int:
        return self.__subject_id

    def get_room_id(self) -> int:
        return self.__room_id

    def get_start_time(self) -> int:
        return self.__start_time

    def get_end_time(self) -> int:
        return self.__end_time

    def get_timetable_id(self) -> int:
        return self.__timetable_id

    def __dict__(self) -> dict:
        return {
            "count_studying_hours": self.get_count_studying_hours(),
            "group_id": self.get_group_id(),
            "subject_id": self.get_subject_id(),
            "room_id": self.get_room_id(),
            "start_time": self.get_start_time(),
            "end_time": self.get_end_time(),
            "timetable_id": self.get_timetable_id(),
            "object_id": self.get_main_id()}

    def __str__(self):
        return f'LessonRow(count_studying_hours={self.get_count_studying_hours()}, group_id={self.get_group_id()}' \
               f', subject_id={self.get_subject_id()}, room_id={self.get_room_id()}), start_time={self.get_start_time()})' \
               f', end_time={self.get_end_time()}), timetable_id={self.get_timetable_id()})' \
               f', object_id={self.get_main_id()})'

    @staticmethod
    def parse(file_location: str, db_source: FileSource) -> List[(Optional[str], Optional[LessonRow])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []
        for i in lines:
            try:
                count_studying_hours = i[0]
                group_id = i[1]
                subject_id = i[2]
                room_id = i[3]
                start_time = i[4]
                end_time = i[5]
                timetable_id = i[6]

                res.append(ParsedData(None, LessonRow(db_source, int(count_studying_hours), int(group_id), int(subject_id),
                                                      int(room_id), int(start_time), int(end_time), int(timetable_id))))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append(ParsedData(exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в LessonRow.parse():\n{e}"
                print(exception_text)
                res.append(ParsedData(exception_text, None))
        return res

    def get_teachers(self) -> List[Teacher]:
        """
            Возвращает список объектов Teacher используя db_source данный в __init__()
            :return: список словарей объектов Teacher
        """
        return TeachersForLessonRows.get_teachers_by_lesson_row_id(self.get_main_id(), self.get_db_source())
