from __future__ import annotations
from typing import TYPE_CHECKING

import logging, psycopg2
from flask import request, jsonify

from schedule_app import app
from data_model.subject import Subject
from data_model.teacher import Teacher
from data_model.teachers_for_subjects import TeachersForSubjects
from validators.subject_validator import SubjectValidator

if TYPE_CHECKING:
    from flask import Response
    from typing import Union, Any, Tuple


validator = SubjectValidator()


@app.route("/api/v1/subjects", methods=["GET"])
def get_subjects() -> Response:
    try:
        result = []
        for i in Subject.get_all(app.config.get("schedule_db_source")):
            subj = i.__dict__()
            subj['teachers'] = [i.__dict__()['object_id'] for i in
                                TeachersForSubjects.get_teachers_by_subject_id(
                                    i.get_main_id(), app.config.get("schedule_db_source")
                                    )]
            result.append(subj)
        return jsonify(result)
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/subject/detailed", methods=["GET"])
def get_subjects_detailed() -> Response:
    try:
        result = []
        for i in Subject.get_all(app.config.get("schedule_db_source")):
            subj = i.__dict__()
            subj['teachers'] = [i.__dict__() for i in
                                TeachersForSubjects.get_teachers_by_subject_id(
                                    i.get_main_id(), app.config.get("schedule_db_source")
                                    )]
            result.append(subj)
        return jsonify(result)
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/subjects/<int:object_id>", methods=["GET"])
def get_subject_by_id(object_id: int) -> Union[Response, Tuple[str, int]]:
    try:
        dct = Subject.get_by_id(source=app.config.get("schedule_db_source"), element_id=object_id).__dict__()
        dct['teachers'] = [i.get_main_id() for i in
                           TeachersForSubjects.get_teachers_by_subject_id(object_id, app.config.get(
                               "schedule_db_source"))]
        return jsonify(dct)
    except ValueError:
        return '', 404


@app.route("/api/v1/subjects", methods=["POST"])
def create_subject() -> Union[Tuple[str, int], Response]:
    ids = []
    req: dict = request.get_json()
    try:
        validator.validate(req, "POST")
    except:
        return "", 400
    try:
        subject = Subject(subject_name=req["subject_name"], source=app.config.get("schedule_db_source")).save()
        if "teachers" in req.keys():
            for elem in req["teachers"]:
                tfs = TeachersForSubjects(subject_id=subject.get_main_id(), teacher_id=int(elem),
                                          source=app.config.get("schedule_db_source")).save()
        result = subject.__dict__()
        result["teachers"] = req["teachers"]
        return jsonify(result)
    except ValueError as e:
        logging.error(e, exc_info=True)
        return "", 404
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/subjects/<int:object_id>", methods=["PUT"])
def update_subject(object_id: int) -> Union[Tuple[str, int], Response]:
    req: dict = request.get_json()

    if request.get_json().get('object_id') != object_id:
        return "", 400

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
        new_subject = Subject(**new_subject, source=app.config.get("schedule_db_source")).save()
        new_subject_dict = new_subject.__dict__()
        new_subject_dict['teachers'] = req_teachers if req_teachers else [i.get_main_id() for i in
                                                                          new_subject.get_teachers()]
        return jsonify(new_subject_dict)
    except ValueError:
        return "", 404
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/subject/detailed/<int:object_id>", methods=["GET"])
def get_teachers_by_subject_id(object_id: int) -> Union[Response, Tuple[str, int]]:
    try:
        dct = Subject.get_by_id(source=app.config.get("schedule_db_source"), element_id=object_id).__dict__()
        dct['teachers'] = [i.__dict__() for i in
                           TeachersForSubjects.get_teachers_by_subject_id(object_id, app.config.get(
                               "schedule_db_source"))]
        return jsonify(dct)
    except ValueError:
        return '', 404


@app.route("/api/v1/subjects/<int:object_id>", methods=["DELETE"])
def delete_subject(object_id) -> Union[Response, Tuple[str, int], Tuple[Any, int]]:
    try:
        subject = Subject.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        subject = subject.delete().__dict__()
        return jsonify(subject)
    except psycopg2.Error as e:
        return jsonify(psycopg2.errorcodes.lookup(e.pgcode)), 409
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500
