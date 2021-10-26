from datetime import date


class NoLearningPeriod:
    def __init__(self, timetableid: int, start: date, stop: date,
                 nolearningperiodid: int = None):
        # Для начала и конца каникул можно использовать только дату
        self.__no_learning_period_id = nolearningperiodid
        self.__startime = start
        self.__stoptime = stop
        self.__timetable_id = timetableid

    def get_no_learning_period_id(self):
        return self.__no_learning_period_id

    def get_startime(self):
        return self.__startime

    def get_stoptime(self):
        return self.__stoptime

    def get_timetable_id(self):
        return self.__timetable_id
