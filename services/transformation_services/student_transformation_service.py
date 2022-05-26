from __future__ import annotations
from typing import TYPE_CHECKING
from data_model.student import Student
from data_model.students_for_groups import StudentsForGroups

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class StudentTransformationService:

    def get_students_transform(self, db_source: DBSource):
        result = []
        for student in Student.get_all(db_source):
            student_data = student.__dict__()
            student_data["groups"] = [group.get_main_id() for group in
                                      StudentsForGroups.get_group_by_student_id(student.get_main_id(), db_source)]
            result.append(student_data)
        return {"students": result}

    def get_students_detailed_transform(self, db_source: DBSource):
        result = []
        for student in Student.get_all(db_source):
            student_data = student.__dict__()
            student_data["groups"] = [group.__dict__() for group in
                                      StudentsForGroups.get_group_by_student_id(student.get_main_id(), db_source)]
            result.append(student_data)
        return {"students": result}

    def get_student_by_id_detailed_transform(self, object_id: int, db_source: DBSource):
        result = Student.get_by_id(object_id, db_source).__dict__()
        result["groups"] = [group.__dict__() for group in
                            StudentsForGroups.get_group_by_student_id(object_id, db_source)]
        return result

    def get_student_by_id_transform(self, object_id: int, db_source: DBSource):
        result = Student.get_by_id(object_id, db_source).__dict__()
        result["groups"] = [group_obj.get_main_id() for group_obj in
                            StudentsForGroups.get_group_by_student_id(object_id, db_source)]
        return result

    def create_student_transform(self, request: dict, db_source: DBSource):
        dct = request
        try:
            groups = dct.pop('groups')
            student = Student(**dct, db_source=db_source).save()
            for i in groups:
                student.append_group_by_id(i)
        except ValueError:
            return '', 404
        dct = student.__dict__()
        dct['groups'] = groups
        return dct

    def update_student_transform(self, object_id: int, request: dict, db_source: DBSource):
        dct = request
        Student.get_by_id(object_id, db_source=db_source)
        groups = []
        if 'groups' in dct:
            groups = dct.pop('groups')
        result = Student(**dct, db_source=db_source, object_id=object_id).save()
        for i in result.get_all_groups():
            if i.get_main_id() not in groups:
                result.remove_group(i)
        for i in groups:
            result.append_group_by_id(group_id=i)
        dct = result.__dict__()
        dct['groups'] = groups
        return dct

    def delete_student_transform(self, object_id: int, db_source: DBSource):
        student = Student.get_by_id(object_id, db_source)
        student = student.delete().__dict__()
        return student
