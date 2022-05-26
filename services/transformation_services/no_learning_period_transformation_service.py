from __future__ import annotations
from typing import TYPE_CHECKING
from data_model.no_learning_period import NoLearningPeriod

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class NoLearningPeriodTransformationService:

    def get_no_learning_period_transform(self, db_source: DBSource):
        return [i.__dict__() for i in NoLearningPeriod.get_all(db_source)]

    def get_no_learning_period_by_id_transform(self, object_id: int, db_source: DBSource):
        return NoLearningPeriod.get_by_id(object_id, db_source).__dict__()

    def create_no_learning_period_transform(self, request: dict, db_source: DBSource):
        return NoLearningPeriod(**request, db_source=db_source).save().__dict__()

    def update_no_learning_period_transform(self, object_id: int, request: dict, db_source: DBSource):
        NoLearningPeriod.get_by_id(object_id, db_source)
        result = NoLearningPeriod(**request, object_id=object_id, db_source=db_source).save().__dict__()
        return result

    def delete_no_learning_period_transform(self, object_id: int, db_source: DBSource):
        period = NoLearningPeriod.get_by_id(object_id, db_source)
        period = period.delete().__dict__()
        return period
