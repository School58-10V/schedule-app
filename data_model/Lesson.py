
class Lesson:
    def __init__(self):
        self.__time =
        self.__day =
        self.__teacher_id =
        self.__lesson_id =
        self.__group_for_lesson_id =
        self.__subject =
        self.__hometask =  # not necessary?
        self.__state = True
        self.__notes =

    def change_state(self):
        self.state = not self.state

    def __get_time(self):
        return self.__time

    def __get_day(self):
        return self.__day

    def __get_teacher_id(self):
        return self.__teacher_id

    def __get_lesson_id(self):
        return self.__lesson_id

    def __get_group_for_lesson_id(self):
        return self.__group_for_lesson_id

    def __get_subject(self):
        return self.__subject

    def __get_hometask(self):
        return self.__hometask

    def __get_state(self):
        return self.__state

    def __get_notes(self):
        return self.__notes
# =)