class TimeTable:
    def __init__(self, year, timetable_id=None):
        self.__table_id = timetable_id
        self.__year = year

    @property
    def table_id(self):
        return self.__table_id
    
    @property
    def year(self):
        return self.__year
