from __future__ import annotations
from typing import TYPE_CHECKING
from data_model.group import Group

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class GroupTransformationService:

    def get_groups_transform(self, db_source: DBSource):
        return [i.__dict__() for i in Group.get_all(db_source=db_source)]

    def get_group_by_id_transform(self, object_id: int, db_source: DBSource):
        return Group.get_by_id(object_id, db_source=db_source).__dict__()

    def create_group_transform(self, request: dict, db_source: DBSource):
        return Group(**request, db_source=db_source).save().__dict__()

    def update_groups_transform(self, object_id: int, request: dict, db_source: DBSource):
        Group.get_by_id(object_id, db_source=db_source)
        return Group(**request, object_id=object_id, db_source=db_source).save().__dict__()

    def delete_group_transform(self, object_id: int, db_source: DBSource):
        return Group.get_by_id(object_id, db_source=db_source).delete().__dict__()
