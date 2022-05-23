from flask import request, jsonify
from schedule_app import app
from validators.group_validator import GroupValidator
from services.transformation_services.group_transformation_service import GroupTransformationService

transform = GroupTransformationService()
validator = GroupValidator()


@app.route("/api/v1/group", methods=["GET"])
def get_groups():
    return jsonify(transform.get_groups_transform())


@app.route("/api/v1/group/<object_id>", methods=["GET"])
def get_group_by_id(object_id):
    try:
        return jsonify(transform.get_group_by_id_transform(object_id))
    except ValueError:
        return '', 404


@app.route("/api/v1/group", methods=["POST"])
def create_group():
    try:
        validator.validate(request.get_json(), "POST")
        return transform.create_group_transform(request.get_json())
    except ValueError:
        return "", 400


@app.route("/api/v1/group/<object_id>", methods=["PUT"])
def update_groups(object_id):
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        return transform.update_groups_transform(object_id, request.get_json())
    except ValueError:
        return "", 404


@app.route("/api/v1/group/<object_id>", methods=["DELETE"])
def delete_group(object_id):
    return transform.delete_group_transform(object_id)
