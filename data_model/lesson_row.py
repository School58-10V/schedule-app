# start_time  начальное время
# end_time конечное время
# num_of_group номер группы
# subject_id айди предмета
# room_id айди комнаты
# timetable_id год в который происходят уроки
# lesson_row_id айди самого класса ряд уроков

class LessonRow:
    def __init__(self, start_time: int, end_time: int, group_id: int, subject_id: int, room_id: int,
                 timetable_id: int, lesson_row_id: int = None):
        self.__start_time = start_time  # start time of lessons (9:00)
        self.__end_time = end_time  # end time of lessons (10:00)
        self.__group_id = group_id  # класс, занимающийся в данный момент.(id группы/класса)
        self.__subject_id = subject_id  # Math. Russian language(id)
        self.__room_id = room_id  # id
        self.__timetable_id = timetable_id  # id
        self.__lesson_row_id = lesson_row_id

    def count_studying_hours(self):
        pass

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

    def get_lesson_row_id(self) -> int:
        return self.__lesson_row_id
