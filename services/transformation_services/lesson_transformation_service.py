from data_model.lesson import Lesson
from schedule_app import app


class LessonTransformationService:

    def get_lessons_trasform(self):
        return [i.__dict__() for i in Lesson.get_all(app.config.get("schedule_db_source"))]

    def get_lesson_by_id_transform(self, object_id: int):
        return Lesson.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()

    def create_lesson_transform(self, request: dict):
        return Lesson(**request, db_source=app.config.get("schedule_db_source")).save().__dict__()

    def update_lessons_transform(self, object_id, request: dict):
        Lesson.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
        return Lesson(**request, object_id=object_id, db_source=app.config.get("schedule_db_source")).save().__dict__()

    def delete_lesson_transform(self, object_id: int):
        lesson = Lesson.get_by_id(object_id, app.config.get("schedule_db_source"))
        lesson = lesson.delete().__dict__()
        return lesson