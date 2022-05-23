from data_model.group import Group
from schedule_app import app


class GroupTransformationService:

    def get_groups_transform(self):
        return [i.__dict__() for i in Group.get_all(app.config.get("schedule_db_source"))]

    def get_group_by_id_transform(self, object_id: int):
        return Group.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()

    def create_group_transform(self, request: dict):
        return Group(**request, db_source=app.config.get("schedule_db_source")).save().__dict__()

    def update_groups_transform(self, object_id: int, request: dict):
        Group.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
        return Group(**request, object_id=object_id, db_source=app.config.get("schedule_db_source")).save().__dict__()

    def delete_group_transform(self, object_id: int):
        return Group.get_by_id(object_id, db_source=app.config.get("schedule_db_source")).delete().__dict__()
