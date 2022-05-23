from data_model.subject import Subject
from data_model.teacher import Teacher
from data_model.teachers_for_subjects import TeachersForSubjects
from schedule_app import app


class SubjectTransformationService:

    def get_subjects_transform(self):
        result = []
        for i in Subject.get_all(app.config.get("schedule_db_source")):
            subj = i.__dict__()
            subj['teachers'] = [i.__dict__()['object_id'] for i in
                                TeachersForSubjects.get_teachers_by_subject_id(
                                    i.get_main_id(), app.config.get("schedule_db_source")
                                )]
            result.append(subj)
        return {'subjects': result}

    def get_subjects_detailed_transform(self):
        result = []
        for i in Subject.get_all(app.config.get("schedule_db_source")):
            subj = i.__dict__()
            subj['teachers'] = [i.__dict__() for i in
                                TeachersForSubjects.get_teachers_by_subject_id(
                                    i.get_main_id(), app.config.get("schedule_db_source")
                                )]
            result.append(subj)
        return {'subjects': result}

    def get_subject_by_id_transform(self, object_id: int):
        return ('teachers', [i.__dict__()['object_id'] for i in
                             TeachersForSubjects.get_teachers_by_subject_id(object_id, app.config.get(
                                 "schedule_db_source"))])

    def create_subject_transform(self, request: dict):
        ids = []
        req: dict = request
        subject = Subject(subject_name=req["subject_name"], db_source=app.config.get("schedule_db_source")).save()
        if "teachers" in req.keys():
            for elem in req["teachers"]:
                tfs = TeachersForSubjects(subject_id=subject.get_main_id(), teacher_id=int(elem),
                                          db_source=app.config.get("schedule_db_source")).save()
                ids.append(tfs.get_main_id())
        result = subject.__dict__()
        result["linker_ids"] = ids
        return result

    def update_subject_transform(self, object_id: int, request: dict):
        req: dict = request
        subject: Subject = Subject.get_by_id(object_id, app.config.get("schedule_db_source"))
        # чистим все поля (искл те которые надо будет добавить) а потом добавляем те которые надо добавить
        saved = []
        if req.get('teachers'):
            for teacher_obj in subject.get_teachers():
                if teacher_obj not in req['teachers']:
                    subject.remove_teacher(teacher_obj)
                else:
                    saved.append(teacher_obj)
            for teacher_id in req['teachers']:
                if teacher_id in saved:
                    continue
                subject.append_teacher(Teacher.get_by_id(teacher_id, app.config.get("schedule_db_source")))

        new_subject = subject.__dict__()
        if req.get('teachers'):
            req_teachers = req.pop('teachers')
        else:
            req_teachers = None

        new_subject.update(req)
        new_subject = Subject(**new_subject, db_source=app.config.get("schedule_db_source")).save()
        new_subject_dict = new_subject.__dict__()
        new_subject_dict['teachers'] = req_teachers if req_teachers else [i.get_main_id() for i in
                                                                          new_subject.get_teachers()]
        return new_subject_dict

    def get_teachers_by_subject_id_transform(self, object_id):
        return ('teachers',
                       [i.__dict__() for i in
                        TeachersForSubjects.get_teachers_by_subject_id(object_id,
                                                                       app.config.get("schedule_db_source"))])

    def delete_subject_transform(self, object_id):
        return Subject.get_by_id(object_id, app.config.get("schedule_db_source")).delete().__dict__()