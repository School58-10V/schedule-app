from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

from data_model.abstract_model import AbstractModel
from data_model.parsed_data import ParsedData
from data_model.students_for_groups import StudentsForGroups
from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from data_model.timetable import TimeTable

if TYPE_CHECKING:
    from adapters.abstract_source import AbstractSource
    from data_model.teacher import Teacher
    from adapters.db_source import DBSource


class LessonRow(AbstractModel):
    def __init__(self, db_source: DBSource, day_of_the_week: int, group_id: int, subject_id: int, room_id: int,
                 start_time: int, end_time: int, timetable_id: int, object_id: Optional[int] = None):
        """
            :param day_of_the_week: день недели (число от 0 до 6)
            :param db_source: Адаптер бд сорса
            :param start_time: начальное время
            :param end_time: конечное время
            :param group_id: номер группы
            :param subject_id: айди предмета
            :param room_id: айди комнаты
            :param timetable_id: год в который происходят уроки
            :param object_id: айди самого класса ряд уроков
        """
        super().__init__(db_source)
        self.__day_of_the_week = day_of_the_week
        self.__start_time = start_time
        self.__end_time = end_time
        self.__group_id = group_id
        self.__subject_id = subject_id
        self.__room_id = room_id
        self.__timetable_id = timetable_id
        self._object_id = object_id

    def get_day_of_the_week(self) -> int:
        return self.__day_of_the_week

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
            "day_of_the_week": self.get_day_of_the_week(),
            "group_id": self.get_group_id(),
            "subject_id": self.get_subject_id(),
            "room_id": self.get_room_id(),
            "start_time": self.get_start_time(),
            "end_time": self.get_end_time(),
            "timetable_id": self.get_timetable_id(),
            "object_id": self.get_main_id()}

    def __repr__(self) -> str:
        return f'LessonRow(day_of_the_week={self.get_day_of_the_week()}, group_id={self.get_group_id()}' \
               f', subject_id={self.get_subject_id()}, room_id={self.get_room_id()}, ' \
               f' start_time={self.get_start_time()}, end_time={self.get_end_time()}, ' \
               f' timetable_id={self.get_timetable_id()}, object_id={self.get_main_id()})'

    def __str__(self) -> str:
        return f'Урок в день недели номер {self.get_day_of_the_week() + 1} который начинается в {self.get_start_time()}'

    @classmethod
    def prettify_time(cls, time):
        """ Превращает тысяча десять в 10:10 """
        hours = time // 100
        minutes = time % 100
        return str(hours).zfill(2) + ':' + str(minutes).zfill(2)

    @staticmethod
    def parse(file_location: str, db_source: DBSource) -> List[(Optional[str], Optional[LessonRow])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []
        for i in lines:
            try:
                day_of_the_week = i[0]
                group_id = i[1]
                subject_id = i[2]
                room_id = i[3]
                start_time = i[4]
                end_time = i[5]
                timetable_id = i[6]

                res.append(ParsedData(None, LessonRow(db_source=db_source,
                                                      day_of_the_week=int(day_of_the_week),
                                                      group_id=int(group_id),
                                                      subject_id=int(subject_id),
                                                      room_id=int(room_id),
                                                      start_time=int(start_time),
                                                      end_time=int(end_time),
                                                      timetable_id=int(timetable_id))))
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

    @classmethod
    def get_all_by_day(cls, week_day: int, db_source: DBSource):
        # TODO: remove? это разве не тоже самое что и LessonRow.get_by_day()
        lessons = [LessonRow.get_by_id(i['object_id'], db_source)
                   for i in db_source.get_by_query(cls._get_collection_name(),
                                                   {"day_of_the_week": week_day})]
        return lessons

    def get_teachers(self) -> List[Teacher]:
        """
            Возвращает список объектов Teacher используя db_source данный в __init__()
            :return: список словарей объектов Teacher
        """
        return TeachersForLessonRows.get_teachers_by_lesson_row_id(self.get_main_id(), self.get_db_source())

    def append_teacher(self, teacher: Teacher) -> LessonRow:
        """
            Добавляем новую связь в TeachersForLessonRows, передавая Teacher.get_main_id() в параметр id
            :return: новый экземпляр класса LessonRow
        """
        instance = TeachersForLessonRows(teacher_id=teacher.get_main_id(),
                                         lesson_row_id=self._object_id, db_source=self.get_db_source())
        for elem in TeachersForLessonRows.get_teachers_by_lesson_row_id(lesson_row_id=self._object_id,
                                                                        db_source=self.get_db_source()):
            if elem.get_main_id() == teacher.get_main_id():
                return self
        instance.save()
        return self

    def remove_teacher(self, teacher: Teacher) -> LessonRow:
        """
            Удаляем связь из TeachersForLessonRows, передавая Teacher.get_main_id() в параметр id
            :return: новый экземпляр класса LessonRow(пустой?)
        """
        for elem in TeachersForLessonRows.get_by_lesson_row_and_teacher_id(lesson_row_id=self.get_main_id(),
                                                                           teacher_id=teacher.get_main_id(),
                                                                           db_source=self.get_db_source()):
            elem.delete()
        return self

    @classmethod
    def get_lesson_rows_by_group_id(cls, group_id: int, db_source: AbstractSource) -> List[LessonRow]:
        """

        :param group_id: идшник группы
        :param db_source: дб_сорс
        :return: список объектов LessonRow где group_id равен указаному
        """
        return [cls(db_source, **i) for i in db_source.get_by_query(cls._get_collection_name(), {'group_id': group_id})]

    @classmethod
    def get_by_day(cls, day: int, db_source: AbstractSource) -> List[LessonRow]:
        lessons = [LessonRow.get_by_id(i['object_id'], db_source)
                   for i in db_source.get_by_query(cls._get_collection_name(), {"day_of_the_week": day})]
        return lessons

    @classmethod
    def get_all_by_student_id(cls, student_id: int, db_source: AbstractSource) -> List[LessonRow]:
        """ возвращает все lessonrow для student """
        group_list = StudentsForGroups.get_group_by_student_id(student_id, db_source)
        lessonrow_list = []
        for i in group_list:
            for lr in db_source.get_by_query(cls._get_collection_name(), {"group_id": i.get_main_id(), "timetable_id": TimeTable.get_current_timetable(db_source).get_main_id()}):
                lessonrow_list.append(LessonRow(db_source, **lr))
        return lessonrow_list

    @classmethod
    def get_by_day_and_student(cls, day: int, student_id: int, db_source: DBSource) -> List[LessonRow]:
        group_ids = [i.get_main_id() for i in StudentsForGroups.get_group_by_student_id(student_id, db_source)]
        lessons = []
        for group_id in group_ids:
            group_lessons = [LessonRow.get_by_id(i['object_id'], db_source)
                             for i in db_source.get_by_query(cls._get_collection_name(),
                                                             {"day_of_the_week": day,
                                                              "group_id": group_id})]
            for lesson in group_lessons:
                lessons.append(lesson)
        return sorted(lessons, key=lambda x: x.get_start_time())
    
    @classmethod
    def get_by_timetable_id(cls, source: AbstractSource, timetable_id: int) -> list:
        return [LessonRow(db_source=source, **elem) for elem in source.get_by_query("LessonRows", {"timetable_id": timetable_id})]
