from datetime import timedelta


class TimeTable:
    def __init__(self, year: timedelta, timetable_id: int = None):
        # Год - период времени
        self.__table_id = timetable_id
        self.__year = year

    def get_table_id(self) -> int:
        return self.__table_id

    def get_year(self) -> timedelta:
        return self.__year
