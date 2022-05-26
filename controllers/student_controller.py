from __future__ import annotations
from typing import TYPE_CHECKING, Union
import psycopg2
from flask import request, jsonify
from psycopg2 import errorcodes
from validators.student_validator import StudentValidator
from services.transformation_services.student_transformation_service import StudentTransformationService

if TYPE_CHECKING:
    from flask import Response

from schedule_app import app

transform = StudentTransformationService()
validator = StudentValidator()
db_source = app.config.get("schedule_db_source")

@app.route("/api/v1/students", methods=["GET"])
def get_students():
    return jsonify(transform.get_students_transform())


@app.route("/api/v1/students/detailed", methods=["GET"])
def get_students_detailed():
    return jsonify(transform.get_students_detailed_transform(db_source))


@app.route("/api/v1/students/get/detailed/<object_id>", methods=["GET"])
def get_student_by_id_detailed(object_id):
    try:
        return jsonify(transform.get_student_by_id_detailed_transform(object_id, db_source))
    except ValueError:
        return "", 404


@app.route("/api/v1/students/<object_id>", methods=["GET"])
def get_student_by_id(object_id):
    try:
        return jsonify(transform.get_student_by_id_transform(object_id, db_source))
    except ValueError:
        return "", 404


@app.route("/api/v1/students", methods=["POST"])
def create_student():
    try:
        validator.validate(request.get_json(), "POST")
    except ValueError:
        return '', 400
    return jsonify(transform.create_student_transform(request.get_json(), db_source))


@app.route("/api/v1/students/<object_id>", methods=["PUT"])
def update_student(object_id: int) -> Union[Response, tuple[str, int]]:
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        return jsonify(transform.update_student_transform(object_id, request.get_json(), db_source))
    except ValueError:
        return "", 404
    except TypeError:
        return "", 400


@app.route("/api/v1/students/<object_id>", methods=["DELETE"])
def delete_student(object_id):
    try:
        return jsonify(transform.delete_student_transform(object_id, db_source))
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        return jsonify(errorcodes.lookup(e.pgcode)), 409
