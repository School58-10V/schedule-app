from data_model.group import Group
from flask import request, jsonify
from schedule_app import app
from validators.group_validator import GroupValidator

validator = GroupValidator()


@app.route("/api/v1/group", methods=["GET"])
def get_groups():
    return jsonify([i.__dict__() for i in Group.get_all(app.config.get("schedule_db_source"))])


@app.route("/api/v1/group/<object_id>", methods=["GET"])
def get_group_by_id(object_id):
    try:
        return jsonify(Group.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
    except ValueError:
        return '', 404


@app.route("/api/v1/group", methods=["POST"])
def create_group():
    try:
        validator.validate(request.get_json(), "POST")
        return Group(**request.get_json(), db_source=app.config.get("schedule_db_source")) \
            .save() \
            .__dict__()
    except ValueError:
        return "", 400


@app.route("/api/v1/group/<object_id>", methods=["PUT"])
def update_groups(object_id):
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


@app.route("/api/v1/group/<object_id>", methods=["DELETE"])
def delete_group(object_id):
    if request.method == 'DELETE':
        return Group.get_by_id(object_id, db_source=app.config.get("schedule_db_source")).delete().__dict__()