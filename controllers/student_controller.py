from __future__ import annotations
from typing import TYPE_CHECKING

import logging, psycopg2
from flask import request, jsonify

from schedule_app import app
from data_model.student import Student
from data_model.students_for_groups import StudentsForGroups
from validators.student_validator import StudentValidator

if TYPE_CHECKING:
    from flask import Response
    from typing import Union, Tuple


validator = StudentValidator()


@app.route("/api/v1/students", methods=["GET"])
def get_students() -> Response:
    try:
        result = []
        for student in Student.get_all(app.config.get("schedule_db_source")):
            student_data = student.__dict__()
            student_data["groups"] = [group.get_main_id() for group in
                                    StudentsForGroups.get_group_by_student_id(student.get_main_id(),
                                                                                app.config.get("schedule_db_source"))]
            result.append(student_data)
        return jsonify(result)
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/students/detailed", methods=["GET"])
def get_students_detailed() -> Response:
    try:
        result = []
        for student in Student.get_all(app.config.get("schedule_db_source")):
            student_data = student.__dict__()
            student_data["groups"] = [group.__dict__() for group in
                                    StudentsForGroups.get_group_by_student_id(student.get_main_id(),
                                                                                app.config.get("schedule_db_source"))]
            result.append(student_data)
        return jsonify(result)
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/students/detailed/<int:object_id>", methods=["GET"])
def get_student_by_id_detailed(object_id: int) -> Tuple[str, int] | Response:
    try:
        result = Student.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
        result["groups"] = [group.__dict__() for group in
                            StudentsForGroups.get_group_by_student_id(object_id, app.config.get("schedule_db_source"))]
    except ValueError:
        return "", 404
    return jsonify(result)


@app.route("/api/v1/students/<int:object_id>", methods=["GET"])
def get_student_by_id(object_id: int) -> Tuple[str, int] | Response:
    try:
        result = Student.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
        result["groups"] = [group_obj.get_main_id() for group_obj in
                            StudentsForGroups.get_group_by_student_id(object_id, app.config.get("schedule_db_source"))]
    except ValueError:
        return "", 404
    return jsonify(result)


@app.route("/api/v1/students", methods=["POST"])
def create_student() -> Tuple[str, int] | Response:
    dct = request.get_json()
    validation_data = validator.validate(dct, "POST")
    if not validation_data[0]:
        return validation_data[1], 400
    try:
        try:
            groups = dct.pop('groups')
            student = Student(**dct, db_source=app.config.get("schedule_db_source")).save()
            for i in groups:
                student.append_group_by_id(i)
        except ValueError as e:
            return "unknown", 404
        dct = student.__dict__()
        dct['groups'] = groups
        return jsonify(dct)
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/students/<int:object_id>", methods=["PUT"])
def update_student(object_id: int) -> Union[Response, Tuple[str, int]]:

    dct = request.get_json()

    if request.get_json().get('object_id') != object_id:
        return "", 400

    validation_data = validator.validate(dct, "PUT")
    if not validation_data[0]:
        return validation_data[1], 400

    try:
        Student.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        groups = []

        if 'groups' in dct:
            groups = dct.pop('groups')
        result = Student(**dct, db_source=app.config.get("schedule_db_source")).save()

        for i in result.get_all_groups():
            if i.get_main_id() not in groups:
                result.remove_group(i)

        for i in groups:
            result.append_group_by_id(group_id=i)

        dct = result.__dict__()
        dct['groups'] = groups
        return jsonify(dct)
    except ValueError:
        return "", 404
    except TypeError:
        return "", 400
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/students/<int:object_id>", methods=["DELETE"])
def delete_student(object_id: int) -> Response | Tuple[str, int] | Tuple[Response, int]:
    try:
        student = Student.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        student = student.delete().__dict__()
        return jsonify(student)
    except psycopg2.Error as e:
        return jsonify(psycopg2.errorcodes.lookup(e.pgcode)), 409
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500
