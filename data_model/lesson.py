from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from data_model.abstract_model import AbstractModel
from typing import List, Optional, TYPE_CHECKING
from data_model.parsed_data import ParsedData

if TYPE_CHECKING:
    from adapters.file_source import FileSource


class Lesson(AbstractModel):

    def __init__(self, db_source: FileSource, start_time: int, end_time: int, day: int, teacher_id: int, group_id: int,
                 subject_id: int, notes: str, object_id: Optional[int] = None, state: Optional[bool] = True):
        """
            :param start_time: начало урока
            :param end_time: конец урока
            :param day: дата
            :param teacher_id: замена
            :param object_id: группа учеников
            :param subject_id: предмет
            :param notes: примечания
            :param group_id: урок
            :param state: состояние
        """
        super().__init__(db_source)
        self.__start_time = start_time
        self.__end_time = end_time
        self.__day = day
        self.__teacher_id = teacher_id
        self.__group_id = group_id
        self.__subject_id = subject_id
        self.__notes = notes
        self._object_id = object_id
        self.__state = state

    def toggle_state(self):
        self.__state = not self.__state

    # get functions

    def get_start_time(self) -> int:
        return self.__start_time

    def get_end_time(self) -> int:
        return self.__end_time

    def get_day(self) -> int:
        return self.__day

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_group_id(self) -> int:
        return self.__group_id

    def get_subject_id(self) -> int:
        return self.__subject_id

    def get_notes(self) -> str:
        return self.__notes

    def get_state(self) -> Optional[bool]:
        return self.__state

    @staticmethod
    def parse(file_location: str, db_source: FileSource) -> List[(Optional[str], Optional[Lesson])]:
        with open(file_location, encoding='utf-8') as file:
            lines = file.read().split('\n')[1:]
            lines = [i.split(';') for i in lines]
            res = []
            for i in lines:
                try:
                    start_time = i[0]
                    end_time = i[1]
                    day = i[2]
                    teacher_id = i[3]
                    group_id = i[4]
                    subject_id = i[5]
                    notes = i[6]
                    state = i[8] == 'True'
                    res.append(ParsedData(None, Lesson(db_source, int(start_time), int(end_time), int(day),
                                                       int(teacher_id), int(group_id), int(subject_id), notes,
                                                       state=state)))

                except IndexError as e:
                    exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                    print(exception_text)
                    print(e)
                    res.append(ParsedData(exception_text, None))
                except Exception as e:
                    exception_text = f"Неизвестная ошибка в Lesson.parse():\n{e}"
                    print(exception_text)
                    res.append(ParsedData(exception_text, None))
            return res

    def __str__(self):
        return f"Урок с id={self._object_id}"

    def __dict__(self) -> dict:
        return {"start_time": self.__start_time,
                "end_time": self.__end_time,
                "day": self.__day,
                "teacher_id": self.__teacher_id,
                "group_id": self.__group_id,
                "subject_id": self.__subject_id,
                "notes": self.__notes,
                "object_id": self._object_id,
                "state": self.__state}
