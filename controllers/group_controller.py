from typing import Tuple, Optional, Union

from data_model.group import Group
from flask import request, jsonify, Response

from data_model.student import Student
from schedule_app import app
from validators.group_validator import GroupValidator
from data_model.students_for_groups import StudentsForGroups

validator = GroupValidator()


@app.route("/api/v1/group", methods=["GET"])
def get_groups() -> Response:
    dct = []
    for i in Group.get_all(app.config.get("schedule_db_source")):
        dct1 = i.__dict__()
        dct1['students'] = []
        for j in i.get_all_students():
            dct1['students'].append(j.get_main_id())
        dct.append(dct1)
    return jsonify(dct)


@app.route("/api/v1/group/<int:object_id>", methods=["GET"])
def get_group_by_id(object_id: int) -> Union[Response, Tuple[str, int]]:
    try:
        group = Group.get_by_id(object_id, app.config.get("schedule_db_source"))
        dct = group.__dict__()
        dct['students'] = [i.get_main_id() for i in group.get_all_students()]
        return jsonify(dct)
    except ValueError:
        return '', 404


@app.route("/api/v1/group", methods=["POST"])
def create_group() -> Union[Response, Tuple[str, int]]:
    try:
        validator.validate(request.get_json(), "POST")
        dct = request.get_json()
        student = []
        if 'students' in dct:
            student = dct.pop('students')
        group = Group(**request.get_json(), db_source=app.config.get("schedule_db_source")) \
            .save()
        for i in student:
            student1 = Student.get_by_id(i, db_source=app.config.get('schedule_db_source'))
            group.append_student(student1)
        dct = group.__dict__()
        dct['students'] = student
        dct['object_id'] = group.get_main_id()
        return jsonify(dct)
    except ValueError:
        return "", 400


@app.route("/api/v1/group/<int:object_id>", methods=["PUT"])
def update_groups(object_id: int) -> Union[Tuple[str, int], Response]:
    if request.get_json().get('object_id') != object_id:
        return "", 400
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        group = Group.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    dct = request.get_json()
    student_id = []
    if 'students' in dct:
        student_id = dct.pop('students')
    old_students_id = [i.get_main_id() for i in group.get_all_students()]
    delete_students = list(set(old_students_id) - set(student_id))
    add_students = list(set(student_id) - set(old_students_id))
    try:
        for i in delete_students:
            student1 = Student.get_by_id(i, db_source=app.config.get('schedule_db_source'))
            group.remove_student(student1)

        for i in add_students:
            student1 = Student.get_by_id(i, db_source=app.config.get('schedule_db_source'))
            group.append_student(student1)

    except ValueError:
        return '', 400

    dct = Group(**dct, db_source=app.config.get('schedule_db_source')).save().__dict__()
    dct['students'] = student_id
    return jsonify(dct)


@app.route("/api/v1/group/<int:object_id>", methods=["DELETE"])
def delete_group(object_id: int) -> Response:
    if request.method == 'DELETE':
        return jsonify(Group.get_by_id(object_id, db_source=app.config.get("schedule_db_source")).delete().__dict__())


@app.route("/api/v1/group/detailed", methods=["GET"])
def get_all_detailed() -> Response:
    global_dct = {'groups': []}
    for i in Group.get_all(app.config.get("schedule_db_source")):
        local_dct = i.__dict__()
        local_dct['students'] = [i.__dict__() for i in StudentsForGroups.get_student_by_group_id(
            i.get_main_id(), db_source=app.config.get("schedule_db_source"))]
        global_dct['groups'].append(local_dct.copy())
    return jsonify(global_dct)


@app.route('/api/v1/group/detailed/<int:object_id>', methods=['GET'])
def get_detailed_group_by_id(object_id: int) -> Union[Response, Tuple[str, int]]:
    """
    Дастаем Group по id вместе со студентами
    :param object_id: int
    :return: Response
    """
    try:
        dct = Group.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
        dct['students'] = [i.__dict__() for i in StudentsForGroups.get_student_by_group_id(
            object_id, db_source=app.config.get("schedule_db_source"))]
        return jsonify(dct)
    except ValueError:
        return '', 404
