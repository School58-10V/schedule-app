class NoLearningPeriod:
    def __init__(self, timetableid, start, stop, nolearningperiodid=None):
        self.__no_learning_period_id = nolearningperiodid
        self.__startime = start
        self.__stoptime = stop
        self.__timetable_id = timetableid

    @property
    def no_learning_period_id(self):
        return self.__no_learning_period_id
    
    @property
    def startime(self):
        return self.__startime
    
    @property
    def stoptime(self):
        return self.__stoptime
    
    @property
    def timetable_id(self):
        return self.__timetable_id
