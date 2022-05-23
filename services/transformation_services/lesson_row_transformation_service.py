from data_model.lesson_row import LessonRow
from data_model.teachers_for_lesson_rows import TeachersForLessonRows
from schedule_app import app


class LessonRowTransformationService:

    def get_all_lesson_rows_transform(self):
        global_dct = {'lesson_rows': []}
        for i in LessonRow.get_all(app.config.get("schedule_db_source")):
            local_dct = i.__dict__()
            local_dct['teachers'] = [i.get_main_id() for i in TeachersForLessonRows.
                get_teachers_by_lesson_row_id(i.get_main_id(), db_source=app.config.get("schedule_db_source"))]
            global_dct['lesson_rows'].append(local_dct.copy())
        return global_dct

    def get_all_detailed_transform(self):
        global_dct = {'lesson_rows': []}
        for i in LessonRow.get_all(app.config.get("schedule_db_source")):
            local_dct = i.__dict__()
            local_dct['teachers'] = [i.__dict__() for i in TeachersForLessonRows.
                get_teachers_by_lesson_row_id(i.get_main_id(), db_source=app.config.get("schedule_db_source"))]
            global_dct['lesson_rows'].append(local_dct.copy())
        return global_dct

    def get_lesson_row_by_id_transform(self, object_id: int):
        dct = LessonRow.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
        dct['teachers'] = [i.get_main_id() for i in TeachersForLessonRows.
            get_teachers_by_lesson_row_id(object_id, db_source=app.config.get("schedule_db_source"))]
        return dct

    def get_detailed_lesson_row_by_id_transform(self, object_id: int):
        dct = LessonRow.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
        dct['teachers'] = [i.__dict__() for i in TeachersForLessonRows.
            get_teachers_by_lesson_row_id(object_id, db_source=app.config.get("schedule_db_source"))]
        return dct

    def create_lesson_row_transform(self, request: dict):
        dct = request
        teacher_id = dct.pop('teachers')
        lesson_row = LessonRow(**dct, db_source=app.config.get("schedule_db_source")).save()
        for i in teacher_id:
            TeachersForLessonRows(lesson_row_id=lesson_row.get_main_id(), teacher_id=i,
                                  db_source=app.config.get("schedule_db_source")).save()
        dct["object_id"] = lesson_row.get_main_id()
        dct['teachers'] = teacher_id
        return dct

    def update_lesson_rows_transform(self, object_id: int, request: dict):
        dct = request
        new_teachers_id = dct.pop("teachers")
        lesson_row_by_id = LessonRow.get_by_id(object_id, app.config.get("schedule_db_source"))
        lesson_row_by_id_dct = lesson_row_by_id.__dict__()
        lesson_row_by_id_dct['teachers'] = [i.get_main_id() for i in lesson_row_by_id.get_teachers()]
        old_teachers_id = lesson_row_by_id_dct.pop("teachers")
        teachers_to_create = list((set(new_teachers_id) - set(old_teachers_id)))
        teachers_to_delete = list((set(old_teachers_id) - set(new_teachers_id)))

        for i in range(len(teachers_to_delete)):
            tflr = TeachersForLessonRows.get_by_lesson_row_and_teacher_id(teacher_id=teachers_to_delete[i],
                                                                          lesson_row_id=object_id,
                                                                          db_source=app.config.get(
                                                                              "schedule_db_source"))
            for j in tflr:
                j.delete()

        for i in teachers_to_create:
            TeachersForLessonRows(lesson_row_id=object_id, teacher_id=i,
                                  db_source=app.config.get("schedule_db_source")).save()

        lesson_row = LessonRow(**dct, object_id=object_id,
                               db_source=app.config.get("schedule_db_source")).save().__dict__()
        lesson_row['teachers'] = new_teachers_id
        return lesson_row

    def delete_lesson_row_transform(self, object_id):
        lesson_row = LessonRow.get_by_id(object_id, app.config.get("schedule_db_source"))
        lesson_row = lesson_row.delete().__dict__()
        return lesson_row

    def check_availability(self, object_id):
        LessonRow.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))