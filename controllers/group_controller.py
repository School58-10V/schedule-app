from __future__ import annotations
from typing import TYPE_CHECKING

import logging, psycopg2
from flask import request, jsonify

from data_model.group import Group
from data_model.student import Student
from data_model.students_for_groups import StudentsForGroups

from schedule_app import app

from validators.group_validator import GroupValidator
from services.logger.messages_templates import MessagesTemplates

if TYPE_CHECKING:
    from flask import Response
    from typing import Tuple, Union


validator = GroupValidator()

LOGGER = logging.getLogger("main.controller")
MESSAGES = MessagesTemplates()
MODEL = "Group"


@app.route("/api/v1/group", methods=["GET"])
def get_groups():
    try:
        dct = []
        for i in Group.get_all(app.config.get("schedule_db_source")):
            dct1 = i.__dict__()
            dct1['students'] = []
            for j in i.get_all_students():
                dct1['students'].append(j.get_main_id())
            dct.append(dct1)
        LOGGER.info(MESSAGES.Controller.Success.get_collect_all_message(MODEL))
        return jsonify(dct)
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_collect_all(MODEL))
        LOGGER.exception(err)
        return "", 500


@app.route("/api/v1/group/<int:object_id>", methods=["GET"])
def get_group_by_id(object_id: int) -> Union[Response, Tuple[str, int]]:
    try:
        group = Group.get_by_id(object_id, app.config.get("schedule_db_source"))
        dct = group.__dict__()
        dct['students'] = [i.get_main_id() for i in group.get_all_students()]
        LOGGER.info(MESSAGES.Controller.Success.get_find_by_id_message(MODEL, object_id))
        return jsonify(dct)
    except ValueError as e:
        LOGGER.error(MESSAGES.Controller.Error.get_find_by_id_message(MODEL))
        LOGGER.exception(e)
        return '', 404


@app.route("/api/v1/group", methods=["POST"])
def create_group() -> Union[Response, Tuple[str, int]]:
    dct = request.get_json()
    validation_data = validator.validate(dct, "POST")
    if not validation_data[0]:
        LOGGER.error(MESSAGES.General.get_validation_error_message(validation_data[1]))
        return validation_data[1], 400
    try:
        student = []
        if 'students' in dct:
            student = dct.pop('students')
        group = Group(**dct, db_source=app.config.get("schedule_db_source")) \
            .save()
        for i in student:
            student1 = Student.get_by_id(i, db_source=app.config.get('schedule_db_source'))
            group.append_student(student1)
        dct = group.__dict__()
        dct['students'] = student
        LOGGER.info(MESSAGES.Controller.Success.get_create_message(MODEL))
        return jsonify(dct)
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_create_message(MODEL))
        LOGGER.exception(err)
        return "", 500


@app.route("/api/v1/group/<int:object_id>", methods=["PUT"])
def update_groups(object_id: int) -> Union[Tuple[str, int], Response]:
    dct = request.get_json()

    validation_data = validator.validate(dct, "PUT")
    if not validation_data[0]:
        LOGGER.error(MESSAGES.General.get_validation_error_message(validation_data[1]))
        return validation_data[1], 400
    try:
        group = Group.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError as e:
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
        LOGGER.exception(e)
        return "", 404

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
        LOGGER.error(MESSAGES.Controller.Error.get_update_message(MODEL))
        LOGGER.exception(e)
        return '', 400

    dct = Group(**dct, db_source=app.config.get('schedule_db_source')).save().__dict__()
    dct['students'] = student_id

    LOGGER.info(MESSAGES.Controller.Success.get_update_message(MODEL))
    return jsonify(dct)


@app.route("/api/v1/group/<int:object_id>", methods=["DELETE"])
def delete_group(object_id: int) -> Response:
    try:
        group = Group.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
        LOGGER.exception(e)
        return "", 404
    try:
        group = group.delete().__dict__()
        LOGGER.info(MESSAGES.Controller.Success.get_delete_message(MODEL))
        return jsonify(group)
    except psycopg2.Error as e:
        LOGGER.error(MESSAGES.Controller.DBError.get_update_message(MODEL, psycopg2.errorcodes.lookup(e.pgcode)))
        LOGGER.exception(e)
        return psycopg2.errorcodes.lookup(e.pgcode), 409
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_update_message(MODEL))
        LOGGER.exception(err)
        return "", 500


@app.route("/api/v1/group/detailed", methods=["GET"])
def get_all_detailed() -> Response:
    global_dct = []
    for i in Group.get_all(app.config.get("schedule_db_source")):
        local_dct = i.__dict__()
        local_dct['students'] = [i.__dict__() for i in StudentsForGroups.get_student_by_group_id(
            i.get_main_id(), db_source=app.config.get("schedule_db_source"))]
        global_dct.append(local_dct.copy())
    LOGGER.info(MESSAGES.Controller.Success.get_collect_all_detailed_message(MODEL))
    return jsonify(global_dct)


@app.route('/api/v1/group/detailed/<int:object_id>', methods=['GET'])
def get_detailed_group_by_id(object_id: int) -> Union[Response, Tuple[str, int]]:
    """
    Достаем Group по id вместе со студентами
    :param object_id: int
    :return: Response
    """
    try:
        dct = Group.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__()
        dct['students'] = [i.__dict__() for i in StudentsForGroups.get_student_by_group_id(
            object_id, db_source=app.config.get("schedule_db_source"))]
        LOGGER.info(f"Found a group by id {object_id} and expanded it")
        return jsonify(dct)
    except ValueError as e:
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
        LOGGER.exception(e)
        return '', 404
