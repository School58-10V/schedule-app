from __future__ import annotations
from typing import TYPE_CHECKING
from data_model.lesson import Lesson

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class LessonTransformationService:

    def get_lessons_trasform(self, db_source: DBSource):
        return [i.__dict__() for i in Lesson.get_all(db_source)]

    def get_lesson_by_id_transform(self, object_id: int, db_source: DBSource):
        return Lesson.get_by_id(object_id, db_source).__dict__()

    def create_lesson_transform(self, request: dict, db_source: DBSource):
        return Lesson(**request, db_source=db_source).save().__dict__()

    def update_lessons_transform(self, object_id, request: dict, db_source: DBSource):
        Lesson.get_by_id(object_id, db_source=db_source)
        return Lesson(**request, object_id=object_id, db_source=db_source).save().__dict__()

    def delete_lesson_transform(self, object_id: int, db_source: DBSource):
        lesson = Lesson.get_by_id(object_id, db_source)
        lesson = lesson.delete().__dict__()
        return lesson
