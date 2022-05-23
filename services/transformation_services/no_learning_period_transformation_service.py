from data_model.no_learning_period import NoLearningPeriod
from schedule_app import app


class NoLearningPeriodTransformationService:

    def get_no_learning_period_transform(self):
        return [i.__dict__() for i in NoLearningPeriod.get_all(app.config.get("schedule_db_source"))]

    def get_no_learning_period_by_id_transform(self, object_id: int):
        return NoLearningPeriod.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()

    def create_no_learning_period_transform(self, request: dict):
        return NoLearningPeriod(**request, db_source=app.config.get("schedule_db_source")).save().__dict__()

    def update_no_learning_period_transform(self, object_id: int, request: dict):
        NoLearningPeriod.get_by_id(object_id, app.config.get("schedule_db_source"))
        result = NoLearningPeriod(**request, db_source=app.config.get("schedule_db_source"),
                                  object_id=object_id).save().__dict__()
        return result

    def delete_no_learning_period_transform(self, object_id: int):
        period = NoLearningPeriod.get_by_id(object_id, app.config.get("schedule_db_source"))
        period = period.delete().__dict__()
        return period