# start_time начало урока
# end_time конец урока
# day дата
# teacher_id замена
# lesson_id урок
# group_id группа учеников
# subject предмет
# state состояние
# notes примечания


class Lesson:
    def __init__(self, start_time: int, end_time: int, day: int, teacher_id: int, group_id: int,
                 subject_id: int, notes: str, lesson_id: int = None):
        self.__start_time = start_time
        self.__end_time = end_time
        self.__day = day
        self.__teacher_id = teacher_id
        self.__lesson_id = lesson_id
        self.__group_id = group_id
        self.__subject_id = subject_id
        self.__state = True
        self.__notes = notes

    def toggle_state(self):
        self.__state = not self.__state

    def get_start_time(self) -> int:
        return self.__start_time

    def get_end_time(self) -> int:
        return self.__end_time

    def get_day(self) -> int:
        return self.__day

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_lesson_id(self) -> int:
        return self.__lesson_id

    def get_group_id(self) -> int:
        return self.__group_id

    def get_subject(self) -> int:
        return self.__subject_id

    def get_state(self) -> bool:
        return self.__state

    def get_notes(self) -> str:
        return self.__notes
