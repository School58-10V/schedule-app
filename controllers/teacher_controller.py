import psycopg2

from validators.teacher_validator import TeacherValidator
from services.transformation_services.teacher_transformation_service import TeacherTransformationService
from flask import request, jsonify

from schedule_app import app

transform = TeacherTransformationService()
validator = TeacherValidator()

@app.route("/api/v1/teachers", methods=["GET"])
def get_teachers():
    return jsonify(transform.get_teachers_transform())


@app.route("/api/v1/teachers/<object_id>", methods=["GET"])
def get_teacher_by_id(object_id):
    try:
        return jsonify(transform.get_teacher_by_id_transform(object_id))
    except ValueError:
        return '', 404


@app.route("/api/v1/teachers/get/detailed", methods=["GET"])
def get_detailed_teachers():
    return jsonify(transform.get_detailed_teachers_transform())


@app.route("/api/v1/teachers/get/detailed/<object_id>", methods=["GET"])
def get_teacher_detailed_by_id(object_id):
    try:
        return transform.get_teacher_detailed_by_id(object_id)
    except ValueError:
        return '', 404


@app.route("/api/v1/teachers", methods=["POST"])
def create_teacher():
    try:
        validator.validate(request.get_json(), "POST")
    except ValueError:
        return '', 400
    try:
        return jsonify(transform.create_teacher_transform(request.get_json()))
    except TypeError:
        return '', 400
    except ValueError:
        return '', 404


@app.route("/api/v1/teachers/<object_id>", methods=["PUT"])
def update_teacher(object_id):
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        return jsonify(transform.update_teacher_transform(object_id, request.get_json()))
    except ValueError:
        return "", 404


@app.route("/api/v1/teachers/<object_id>", methods=["DELETE"])
def delete_teacher(object_id):
    try:
        return transform.delete_teacher_transform(object_id)
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400
