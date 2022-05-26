from __future__ import annotations
from typing import TYPE_CHECKING
from data_model.teacher import Teacher
from data_model.teachers_for_subjects import TeachersForSubjects
from data_model.teachers_for_lesson_rows import TeachersForLessonRows

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class TeacherTransformationService:

    def get_teachers_transform(self, db_source: DBSource):
        teachers = []
        for i in Teacher.get_all(db_source):
            teacher = i.__dict__()
            teacher['subject_id'] = [j.get_main_id() for j in TeachersForSubjects.
                get_subjects_by_teacher_id(i.get_main_id(),
                                           db_source=db_source)]
            teacher['lesson_row_id'] = [j.get_main_id() for j in TeachersForLessonRows.
                get_lesson_rows_by_teacher_id(i.get_main_id(),
                                              db_source=db_source)]
            teachers.append(teacher)
        return {"teachers": teachers}

    def get_teacher_by_id_transform(self, object_id: int, db_source: DBSource):
        teacher = Teacher.get_by_id(object_id, db_source).__dict__()
        teacher['subject_id'] = [i.get_main_id() for i in TeachersForSubjects.
            get_subjects_by_teacher_id(object_id,
                                       db_source=db_source)]
        teacher['lesson_row_id'] = [i.get_main_id() for i in TeachersForLessonRows.
            get_lesson_rows_by_teacher_id(object_id,
                                          db_source=db_source)]
        return teacher

    def get_detailed_teachers_transform(self, db_source: DBSource):
        teachers = []
        for i in Teacher.get_all(db_source):
            object_id = i.get_main_id()
            teacher = Teacher.get_by_id(object_id, db_source).__dict__()
            teacher['subject'] = [i.__dict__() for i in TeachersForSubjects.
                get_subjects_by_teacher_id(object_id,
                                           db_source=db_source)]
            teacher['lesson_row'] = [i.__dict__() for i in TeachersForLessonRows.
                get_lesson_rows_by_teacher_id(object_id,
                                              db_source=db_source)]
            teachers.append(teacher)
        return {"teachers": teachers}

    def get_teacher_detailed_by_id(self, object_id: int, db_source: DBSource):
        teacher = Teacher.get_by_id(object_id, db_source).__dict__()
        teacher['subject_id'] = [i.__dict__() for i in TeachersForSubjects.
            get_subjects_by_teacher_id(object_id,
                                       db_source=db_source)]
        teacher['lesson_row_id'] = [i.__dict__() for i in TeachersForLessonRows.
            get_lesson_rows_by_teacher_id(object_id,
                                          db_source=db_source)]
        return teacher

    def create_teacher_transform(self, request: dict, db_source: DBSource):
        dct = request
        subject_id = dct.pop('subject_id')
        lesson_row_id = dct.pop('lesson_row_id')

        new_teacher = Teacher(**dct, db_source=db_source).save()

        for i in subject_id:
            TeachersForSubjects(teacher_id=new_teacher.get_main_id(), subject_id=i,
                                db_source=db_source).save()

        for i in lesson_row_id:
            TeachersForLessonRows(teacher_id=new_teacher.get_main_id(), lesson_row_id=i,
                                  db_source=db_source).save()

        new_teacher_dct = new_teacher.__dict__()
        new_teacher_dct['subject_id'] = subject_id
        new_teacher_dct['lesson_row_id'] = lesson_row_id

        return new_teacher_dct

    def update_teacher_transform(self, object_id: int, request: dict, db_source: DBSource):
        teacher = Teacher.get_by_id(object_id, db_source).__dict__()
        teacher['subject_id'] = [i.get_main_id() for i in TeachersForSubjects.
            get_subjects_by_teacher_id(object_id, db_source=db_source)]
        teacher['lesson_row_id'] = [i.get_main_id() for i in TeachersForLessonRows.
            get_lesson_rows_by_teacher_id(object_id,
                                          db_source=db_source)]

        for i in request['subject_id']:
            if i not in teacher['subject_id']:
                TeachersForSubjects(teacher_id=object_id, subject_id=i,
                                    db_source=db_source).save()

        for i in request['lesson_row_id']:
            if i not in teacher['lesson_row_id']:
                TeachersForLessonRows(teacher_id=object_id, lesson_row_id=i,
                                      db_source=db_source).save()

        return Teacher.get_by_id(object_id, db_source).__dict__()

    def delete_teacher_transform(self, object_id: int, db_source: DBSource):
        return Teacher.get_by_id(object_id, db_source).delete().__dict__()
