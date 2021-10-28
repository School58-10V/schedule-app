from datetime import date


class NoLearningPeriod:
    def __init__(self, timetable_id: int, start: date, stop: date,
                 no_learning_period_id: int = None):
        # Для начала и конца каникул можно использовать только дату
        self.__no_learning_period_id = no_learning_period_id
        self.__star_time = start
        self.__stop_time = stop
        self.__timetable_id = timetable_id

    def get_no_learning_period_id(self) -> int:
        return self.__no_learning_period_id

    def get_star_time(self) -> date:
        return self.__star_time

    def get_stop_time(self) -> date:
        return self.__stop_time

    def get_timetable_id(self) -> int:
        return self.__timetable_id
