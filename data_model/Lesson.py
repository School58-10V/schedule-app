class Lesson:
    def __init__(self, start_time: int, end_time: int, day: int, teacher_id: int, lesson_id: int, group_id: int,
                 subject_id: int, notes: str):
        self.__start_time = start_time
        self.__end_time = end_time
        self.__day = day
        self.__teacher_id = teacher_id
        self.__lesson_id = lesson_id
        self.__group_id = group_id
        self.__subject_id = subject_id
        self.__state = True
        self.__notes = notes

    def change_state(self):
        self.__state = not self.__state

    def get_time(self):
        return self.__start_time, self.__end_time

    def get_day(self):
        return self.__day

    def get_teacher_id(self):
        return self.__teacher_id

    def get_lesson_id(self):
        return self.__lesson_id

    def get_group_id(self):
        return self.__group_id

    def get_subject(self):
        return self.__subject_id

    def get_state(self):
        return self.__state

    def get_notes(self):
        return self.__notes
