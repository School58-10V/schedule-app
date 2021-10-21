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
        self.time =
        self.day =
        self.teacher_id =
        self.lesson_id =
        self.group_for_lesson_id =
        self.subject =
        self.hometask =  # not necessary?
        self.state = True
        self.notes =

    def change_state(self):
        self.state = not self.state