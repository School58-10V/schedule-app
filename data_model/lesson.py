from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from data_model.abstract_model import AbstractModel
from typing import List, Optional, TYPE_CHECKING
from data_model.parsed_data import ParsedData
import datetime
from data_model.teacher import Teacher

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class Lesson(AbstractModel):

    def __init__(self, db_source: DBSource, start_time: int, end_time: int, date: datetime.date, teacher_id: int,
                 group_id: int,
                 subject_id: int, notes: str, object_id: Optional[int] = None, state: Optional[bool] = True):
        """
            :param start_time: начало урока
            :param end_time: конец урока
            :param date: дата
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
        self.__date = date
        self.__teacher_id = teacher_id
        self.__group_id = group_id
        self.__subject_id = subject_id
        self.__notes = notes
        self._object_id = object_id
        self.__state = state

    # ??????????????????????????????????????????????????????????
    # https://images-ext-1.discordapp.net/external/lR9qvPvWI0m4EOeoTi9tmB6x91nFQKosP-ElStH8ybY/https/media.tenor.com/JZxEu1mBeGwAAAPo/esqueleto.mp4
    def get_room_id(self) -> int:
        return 1  # Иначе возвращает ошибку, т к у нас в базе данных не может быть кабинет с id None

    def toggle_state(self):
        self.__state = not self.__state

    # get functions

    def get_start_time(self) -> int:
        return self.__start_time

    def get_end_time(self) -> int:
        return self.__end_time

    def get_date(self) -> datetime.date:
        return self.__date  # .strftime('%Y-%m-%d')

    # При вставке в базу данных он сам преобразует дату в строку

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
    def parse(file_location: str, db_source: DBSource) -> List[(Optional[str], Optional[Lesson])]:
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
                    state = i[7] == 'True'
                    res.append(ParsedData(None, Lesson(db_source=db_source,
                                                       start_time=int(start_time),
                                                       end_time=int(end_time),
                                                       date=datetime.datetime.strptime(day, "%Y-%m-%d").date(),
                                                       teacher_id=int(teacher_id),
                                                       group_id=int(group_id),
                                                       subject_id=int(subject_id),
                                                       notes=notes,
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

    def __str__(self) -> str:
        return f"Урок с который начинается в {self.get_start_time()} и заканчивается в {self.get_end_time()}, " \
               f"id={self.get_main_id()}"

    def __dict__(self) -> dict:
        return {"start_time": self.get_start_time(),
                "end_time": self.get_end_time(),
                "date": self.get_date(),
                "teacher_id": self.get_teacher_id(),
                "group_id": self.get_group_id(),
                "subject_id": self.get_subject_id(),
                "notes": self.get_notes(),
                "object_id": self.get_main_id(),
                "state": self.get_state()}

    @classmethod
    def get_today_replacements(cls, db_source: DBSource, date: datetime.date = datetime.date.today()) -> List[Lesson]:
        replacements = [Lesson.get_by_id(i['object_id'], db_source)
                        for i in db_source.get_by_query(cls._get_collection_name(),
                                                        {"day": date})]
        return replacements

    @classmethod
    def get_replacements_by_teacher(cls, db_source: DBSource, teacher: str,
                                    date: datetime.date = datetime.date.today()) -> List[Lesson]: # если ошибка в типе, я лох
        replacements_today = [Lesson.get_by_id(i['object_id'], db_source)
                              for i in db_source.get_by_query(cls._get_collection_name(),
                                                              {"day": date})]
        teacher_info = Teacher.get_by_name(teacher, db_source)
        teacher_id = teacher_info[0].get_main_id()
        # replacements = ', '.join([replacements_today
        #                            for i in db_source.get_by_query(cls._get_collection_name(),
        #                                                 {'teacher_id': teacher_id})])
        res = [i for i in replacements_today if i.get_teacher_id() == teacher_id]
        return res
