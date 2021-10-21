import random


class TimeTable:
    def __init__(self):
        self.__table_id = random.randrange(0, 350000)
        self.__year = "0-0"

    @property
    def getter(self):
        return f"id расписания: {self.__table_id}, учебный год: {self.__year}"


class Day:
    def __init__(self):
        self.__day_id = random.randrange(1, 345678987)
        self.__lessons = {"class_id": ["lessons_id"]}

    @property
    def getter(self):
        return f"id дня: {self.__day_id}, расписание на день: {self.__lessons}"


class NoLearningPeriod:
    def __init__(self):
        self.__no_learning_period_id = random.randrange(1, 8400000)
        self.__start_stop = "0.0.0-0.0.0"
        self.__timetable_id = "получить откуда-то"

    @property
    def getter(self):
        return f"id неучебного периода: {self.__no_learning_period_id}, время начала: {self.__start_stop}, id " \
               f"расписания: {self.__timetable_id}"
