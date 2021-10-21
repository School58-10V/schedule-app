class SeriesOfLessons:
    def __init__(self):
        self.__num_of_group =
        self.__teacher =
        self.__group_right_now =  # класс, занимающийся в данный момент.(id группы/класса)
        self.__theme_of_lesson =  # Math. Russian language
        self.__room =
        self.__time_of_a_lesson =
        self.__timetable =
        self.__num_of_studying_hours =
        self.__id_for_group_of_lessons =

    def __get_num_of_group_id(self):
        return self.__num_of_group

    def __get_teacher_id(self):
        return self.__teacher

    def __get_group_right_now_id(self):
        return self.__group_right_now

    def __get_theme_of_lesson_id(self):
        return self.__theme_of_lesson

    def __get_room_id(self):
        return self.__room

    def __get_time_of_A_lesson_id(self):
        return self.__time_of_a_lesson

    def __get_num_of_studying_hours(self):
        return self.__num_of_studying_hours

    def __get_id_for_group_of_lssons(self):
        return self.__id_for_group_of_lessons


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