
class Lesson:
    def __init__(self, ):
        self.__start_time =
        self.__end_time =
        self.__day =
        self.__teacher_id =  #замена
        self.__lesson_id =
        self.__group_for_lesson_id =
        self.__subject =
        self.__state = True
        self.__notes =

    def change_state(self):
        self.__state = not self.__state

    def get_time(self):
        return self.__time

    def get_day(self):
        return self.__day

    def get_teacher_id(self):
        return self.__teacher_id

    def get_lesson_id(self):
        return self.__lesson_id

    def get_group_for_lesson_id(self):
        return self.__group_for_lesson_id

    def get_subject(self):
        return self.__subject

    def get_state(self):
        return self.__state

    def get_notes(self):
        return self.__notes