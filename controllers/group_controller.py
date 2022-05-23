from typing import Tuple, Optional, Union

from data_model.group import Group
from flask import request, jsonify, Response
from schedule_app import app
from validators.group_validator import GroupValidator
from data_model.students_for_groups import StudentsForGroups

validator = GroupValidator()


@app.route("/api/v1/group", methods=["GET"])
def get_groups() -> Response:
    return jsonify([i.__dict__() for i in Group.get_all(app.config.get("schedule_db_source"))])


@app.route("/api/v1/group/<int:object_id>", methods=["GET"])
def get_group_by_id(object_id: int) -> Union[Response, Tuple[str, int]]:
    try:
        return jsonify(Group.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
    except ValueError:
        return '', 404


@app.route("/api/v1/group", methods=["POST"])
def create_group() -> Union[dict, Tuple[str, int]]:
    try:
        validator.validate(request.get_json(), "POST")
        return Group(**request.get_json(), db_source=app.config.get("schedule_db_source")) \
            .save() \
            .__dict__()
    except ValueError:
        return "", 400


@app.route("/api/v1/group/<int:object_id>", methods=["PUT"])
def update_groups(object_id: int) -> Union[Tuple[str, int], dict]:
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        Group.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
        return Group(**request.get_json(), object_id=object_id, db_source=app.config.get("schedule_db_source")) \
            .save() \
            .__dict__()
    except ValueError:
        return "", 404


@app.route("/api/v1/group/<int:object_id>", methods=["DELETE"])
def delete_group(object_id: int) -> dict:
    if request.method == 'DELETE':
        return Group.get_by_id(object_id, db_source=app.config.get("schedule_db_source")).delete().__dict__()


@app.route("/api/v1/group/detailed", methods=["GET"])
def get_all_detailed() -> Response:
    global_dct = {'groups': []}
    for i in Group.get_all(app.config.get("schedule_db_source")):
        local_dct = i.__dict__()
        local_dct['students'] = [i.__dict__() for i in StudentsForGroups.
            get_student_by_group_id(i.get_main_id(), db_source=app.config.get("schedule_db_source"))]
        global_dct['groups'].append(local_dct.copy())
    return jsonify(global_dct)
