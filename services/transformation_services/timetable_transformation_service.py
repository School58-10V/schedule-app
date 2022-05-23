from data_model.timetable import TimeTable
from schedule_app import app


class TimeTableTransformationService:

    def get_timetable_transform(self):
        return [i.__dict__() for i in TimeTable.get_all(app.config.get("schedule_db_source"))]

    def get_timetable_by_id_transform(self, object_id: int):
        return TimeTable.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()

    def create_timetable_transform(self, request: dict):
        return TimeTable(**request, db_source=app.config.get("schedule_db_source")).save().__dict__()

    def update_timetable_transform(self, object_id: int, request: dict):
        TimeTable.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
        return TimeTable(**request, object_id=object_id,
                         db_source=app.config.get("schedule_db_source")).save().__dict__()

    def delete_timetable_transform(self, object_id: int):
        return TimeTable.get_by_id(object_id, db_source=app.config.get("schedule_db_source")).delete().__dict__()