from __future__ import annotations
from typing import TYPE_CHECKING, Union, Tuple
import psycopg2
from flask import request, jsonify, Response
from psycopg2 import errorcodes
from data_model.student import Student
from data_model.students_for_groups import StudentsForGroups
from validators.student_validator import StudentValidator

if TYPE_CHECKING:
    from flask import Response

from schedule_app import app

validator = StudentValidator()


@app.route("/api/v1/students", methods=["GET"])
def get_students() -> Response:
    result = []
    for student in Student.get_all(app.config.get("schedule_db_source")):
        student_data = student.__dict__()
        student_data["groups"] = [group.get_main_id() for group in
                                  StudentsForGroups.get_group_by_student_id(student.get_main_id(),
                                                                            app.config.get("schedule_db_source"))]
        result.append(student_data)
    return jsonify(result)


@app.route("/api/v1/students/detailed", methods=["GET"])
def get_students_detailed() -> Response:
    result = []
    for student in Student.get_all(app.config.get("schedule_db_source")):
        student_data = student.__dict__()
        student_data["groups"] = [group.__dict__() for group in
                                  StudentsForGroups.get_group_by_student_id(student.get_main_id(),
                                                                            app.config.get("schedule_db_source"))]
        result.append(student_data)
    return jsonify(result)


@app.route("/api/v1/students/get/detailed/<int:object_id>", methods=["GET"])
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
    try:
        validator.validate(dct, "POST")
    except ValueError:
        return '', 400
    try:
        groups = []
        if 'groups' in dct:
            groups = dct.pop('groups')
        student = Student(**dct, db_source=app.config.get("schedule_db_source")).save()
        for i in groups:
            student.append_group_by_id(i)
    except ValueError:
        return '', 404
    dct = student.__dict__()
    dct['groups'] = groups
    return jsonify(dct)


@app.route("/api/v1/students/<int:object_id>", methods=["PUT"])
def update_student(object_id: int) -> Union[Response, Tuple[str, int]]:

    dct = request.get_json()

    if request.get_json().get('object_id') != object_id:
        return "", 400

    try:
        validator.validate(dct, "PUT")

    except ValueError:
        return "", 400

    try:
        Student.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
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


@app.route("/api/v1/students/<int:object_id>", methods=["DELETE"])
def delete_student(object_id: int) -> Response | Tuple[str, int] | Tuple[Response, int]:
    try:
        student = Student.get_by_id(object_id, app.config.get("schedule_db_source"))
        student = student.delete().__dict__()
        return jsonify(student)
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        return jsonify(errorcodes.lookup(e.pgcode)), 409
