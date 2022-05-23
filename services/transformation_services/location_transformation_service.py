from data_model.location import Location
from schedule_app import app


class LocationTransformationService:

    def update_location_transform(self, object_id: int, request: dict):
        Location.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
        return Location(**request, object_id=object_id,
                        db_source=app.config.get("schedule_db_source")).save().__dict__()

    def get_locations_transform(self):
        return [i.__dict__() for i in Location.get_all(app.config.get("schedule_db_source"))]

    def get_location_by_id_transform(self, object_id: int):
        return Location.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()

    def create_location_transform(self, request: dict):
        return Location(**request, db_source=app.config.get("schedule_db_source")).save().__dict__()

    def delete_location_transform(self, object_id):
        location = Location.get_by_id(object_id, app.config.get("schedule_db_source"))
        location = location.delete().__dict__()
        return location
