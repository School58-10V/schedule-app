import psycopg2
from flask import request, jsonify
from validators.subject_validator import SubjectValidator
from services.transformation_services.subject_transformation_service import SubjectTransformationService

from schedule_app import app

transform = SubjectTransformationService()
validator = SubjectValidator()
db_source = app.config.get("schedule_db_source")


@app.route("/api/v1/subjects", methods=["GET"])
def get_subjects():
    return jsonify(transform.get_subjects_transform(db_source))


@app.route("/api/v1/subject/detailed", methods=["GET"])
def get_subjects_detailed():
    return jsonify(transform.get_subjects_detailed_transform(db_source))


@app.route("/api/v1/subjects/<object_id>", methods=["GET"])
def get_subject_by_id(object_id):
    try:
        return jsonify(transform.get_subject_by_id_transform(object_id, db_source))
    except ValueError:
        return '', 404


@app.route("/api/v1/subjects", methods=["POST"])
def create_subject():
    try:
        validator.validate(request.get_json(), "POST")
    except ValueError:
        return "", 400
    try:
        return jsonify(transform.create_subject_transform(request.get_json(), db_source))
    except TypeError as e:
        print(e)
        return "", 400
    except ValueError as e:
        print(e)
        return "", 400


@app.route("/api/v1/subjects/<object_id>", methods=["PUT"])
def update_subject(object_id):
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        return jsonify(transform.update_subject_transform(object_id, request.get_json(), db_source))
    except ValueError:
        return "", 404
    except TypeError:
        return "", 400


@app.route("/api/v1/subject/detailed/<object_id>", methods=["GET"])
def get_teachers_by_subject_id(object_id):
    try:
        return jsonify(transform.get_teachers_by_subject_id_transform(object_id, db_source))
    except ValueError:
        return '', 404


@app.route("/api/v1/subjects/<object_id>", methods=["DELETE"])
def delete_subject(object_id):
    try:
        return transform.delete_subject_transform(object_id, db_source)
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400
