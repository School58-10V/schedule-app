from __future__ import annotations
from typing import TYPE_CHECKING
from data_model.location import Location

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class LocationTransformationService:

    def update_location_transform(self, object_id: int, request: dict, db_source: DBSource):
        Location.get_by_id(object_id, db_source=db_source)
        return Location(**request, object_id=object_id,
                        db_source=db_source).save().__dict__()

    def get_locations_transform(self, db_source: DBSource):
        return [i.__dict__() for i in Location.get_all(db_source)]

    def get_location_by_id_transform(self, object_id: int, db_source: DBSource):
        return Location.get_by_id(object_id, db_source).__dict__()

    def create_location_transform(self, request: dict, db_source: DBSource):
        return Location(**request, db_source=db_source).save().__dict__()

    def delete_location_transform(self, object_id: int, db_source: DBSource):
        location = Location.get_by_id(object_id, db_source)
        location = location.delete().__dict__()
        return location
