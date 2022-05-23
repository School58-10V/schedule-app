from typing import Union, Any

import psycopg2
from flask import request, jsonify, Response
from validators.subject_validator import SubjectValidator
from data_model.subject import Subject
from data_model.teacher import Teacher
from data_model.teachers_for_subjects import TeachersForSubjects

from schedule_app import app

validator = SubjectValidator()


@app.route("/api/v1/subjects", methods=["GET"])
def get_subjects() -> Response:
    result = []
    for i in Subject.get_all(app.config.get("schedule_db_source")):
        subj = i.__dict__()
        subj['teachers'] = [i.__dict__()['object_id'] for i in
                            TeachersForSubjects.get_teachers_by_subject_id(
                                i.get_main_id(), app.config.get("schedule_db_source")
                                )]
        result.append(subj)
    return jsonify({'subjects': result})


@app.route("/api/v1/subject/detailed", methods=["GET"])
def get_subjects_detailed() -> Response:
    result = []
    for i in Subject.get_all(app.config.get("schedule_db_source")):
        subj = i.__dict__()
        subj['teachers'] = [i.__dict__() for i in
                            TeachersForSubjects.get_teachers_by_subject_id(
                                i.get_main_id(), app.config.get("schedule_db_source")
                                )]
        result.append(subj)
    return jsonify({'subjects': result})


@app.route("/api/v1/subjects/<object_id>", methods=["GET"])
def get_subject_by_id(object_id) -> Union[Response, tuple[str, int]]:
    try:
        dct = Subject.get_by_id(db_source=app.config.get("schedule_db_source"), element_id=object_id).__dict__()
        dct['teachers'] = [i.__dict__()['object_id'] for i in
                           TeachersForSubjects.get_teachers_by_subject_id(object_id, app.config.get(
                               "schedule_db_source"))]
        return jsonify(dct)
    except ValueError:
        return '', 404


@app.route("/api/v1/subjects", methods=["POST"])
def create_subject() -> Union[tuple[str, int], Response]:
    ids = []
    req: dict = request.get_json()
    try:
        validator.validate(req, "POST")
    except:
        return "", 400
    try:
        subject = Subject(subject_name=req["subject_name"], db_source=app.config.get("schedule_db_source")).save()
        if "teachers" in req.keys():
            for elem in req["teachers"]:
                tfs = TeachersForSubjects(subject_id=subject.get_main_id(), teacher_id=int(elem),
                                          db_source=app.config.get("schedule_db_source")).save()
                ids.append(tfs.get_main_id())
        result = subject.__dict__()
        result["linker_ids"] = ids
        return jsonify(result)
    except TypeError as e:
        print(e)
        return "", 400
    except ValueError as e:
        print(e)
        return "", 400


@app.route("/api/v1/subjects/<object_id>", methods=["PUT"])
def update_subject(object_id) -> Union[tuple[str, int], Response]:
    req: dict = request.get_json()
    try:
        validator.validate(req, "PUT")
    except:
        return "", 400
    try:

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
        if 'teachers' in req:
            req_teachers = req.pop('teachers')
        else:
            req_teachers = None

        new_subject.update(req)
        new_subject = Subject(**new_subject, db_source=app.config.get("schedule_db_source")).save()
        new_subject_dict = new_subject.__dict__()
        new_subject_dict['teachers'] = req_teachers if req_teachers else [i.get_main_id() for i in
                                                                          new_subject.get_teachers()]
        return jsonify(new_subject_dict)
    except ValueError as e:
        return "", 404
    except TypeError:
        return "", 400


@app.route("/api/v1/subject/detailed/<object_id>", methods=["GET"])
def get_teachers_by_subject_id(object_id) -> Union[Response, tuple[str, int]]:
    try:
        return jsonify('teachers',
                       [i.__dict__() for i in
                        TeachersForSubjects.get_teachers_by_subject_id(object_id,
                                                                       app.config.get("schedule_db_source"))])
    except ValueError:
        return '', 404


@app.route("/api/v1/subjects/<object_id>", methods=["DELETE"])
def delete_subject(object_id) -> Union[dict, tuple[str, int], tuple[Any, int]]:
    try:
        return Subject.get_by_id(object_id, app.config.get("schedule_db_source")).delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400
