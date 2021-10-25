# start_time  начальное время
# end_time конечное время
# num_of_group номер группы
# teacher Учитель закреплённый за рядом урока
# group_right_now класс, занимающийся в данный момент.
# subject_id айди предмета
# room_id айди комнаты
# timetable_id год в который происходят уроки
# __lessonRow_id айди самого класса ряд уроков

class LessonRow:
    def __init__(self, start_time: int, end_time: int, group_id: int, subject_id: int, room_id: int,
                 timetable_id: int, lessonRow_id: int, teacher: ID):
        self.__start_time = start_time  # start time of lessons (9:00)
        self.__end_time = end_time  # end time of lessons (10:00)
        self.__group_id = group_id  # класс, занимающийся в данный момент.(id группы/класса)
        self.__subject_id = subject_id  # Math. Russian language(id)
        self.__room_id = room_id  # id
        self.__timetable_id = timetable_id  # id
        self.__lessonRow_id = lessonRow_id
        self.__teacher = teacher

    def count_studying_hours(self):
        pass

    def get_num_of_group_id(self):
        return self.__num_of_group

    def get_teacher_id(self):
        return self.__teacher

    def get_group_right_now_id(self):
        return self.__group_id

    def get_theme_of_lesson_id(self):
        return self.__theme_of_lesson

    def get_room_id(self):
        return self.__room

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_num_of_studying_hours(self):
        return self.__num_of_studying_hours

    def get_lessonRow_id(self):
        return self.__lessonRow_id
