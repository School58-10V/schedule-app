from __future__ import annotations
from typing import TYPE_CHECKING
from data_model.timetable import TimeTable

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class TimeTableTransformationService:

    def get_timetable_transform(self, db_source: DBSource):
        return [i.__dict__() for i in TimeTable.get_all(db_source)]

    def get_timetable_by_id_transform(self, object_id: int, db_source: DBSource):
        return TimeTable.get_by_id(object_id, db_source).__dict__()

    def create_timetable_transform(self, request: dict, db_source: DBSource):
        return TimeTable(**request, db_source=db_source).save().__dict__()

    def update_timetable_transform(self, object_id: int, request: dict, db_source: DBSource):
        TimeTable.get_by_id(object_id, db_source=db_source)
        return TimeTable(**request, object_id=object_id,
                         db_source=db_source).save().__dict__()

    def delete_timetable_transform(self, object_id: int, db_source: DBSource):
        return TimeTable.get_by_id(object_id, db_source=db_source).delete().__dict__()
