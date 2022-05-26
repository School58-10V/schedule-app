from __future__ import annotations
from validators.location_validator import LocationValidator
from services.transformation_services.location_transformation_service import LocationTransformationService
from typing import TYPE_CHECKING, Union, Any
from flask import request, jsonify
import psycopg2
from psycopg2 import errorcodes

if TYPE_CHECKING:
    from flask import Response

from schedule_app import app

transform = LocationTransformationService()
validator = LocationValidator()
db_source = app.config.get("schedule_db_source")

@app.route("/api/v1/location/<object_id>", methods=['PUT'])
def update_location(object_id: int) -> Union[tuple[str, int], Response]:
    """
    Обновляем Location
    :param object_id: int
    :return: Response
    """
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        return jsonify(transform.update_location_transform(object_id, request.get_json(), db_source))
    except ValueError:
        return "", 404


@app.route("/api/v1/location", methods=["GET"])
def get_locations() -> Response:
    """
        Выдаём все Locations
        :return: Response
    """
    return jsonify(transform.get_locations_transform(db_source))


@app.route("/api/v1/location/<object_id>", methods=["GET"])
def get_location_by_id(object_id: int) -> Union[Response, tuple[str, int]]:
    """
    Выдаём Location по заданному id
    :param object_id: int
    :return: Response
    """
    try:
        return jsonify(transform.get_location_by_id_transform(object_id, db_source))
    except ValueError:
        return '', 404


@app.route("/api/v1/location", methods=["POST"])
def create_location() -> Response():
    """
    Создаём Location по заданным аргументам
    :return: Response
    """
    try:
        validator.validate(request.get_json(), "POST")
        return jsonify(transform.create_location_transform(request.get_json(), db_source))
    except ValueError:
        return "", 400


@app.route("/api/v1/location/<object_id>", methods=["DELETE"])
def delete_location(object_id: int) -> Union[tuple[str, int], tuple[Any, int], Response]:
    """
    Удаляем Location по заданному id
    :param object_id: int
    :return: Response
    """
    try:
        return jsonify(transform.delete_location_transform(object_id, db_source))
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        return errorcodes.lookup(e.pgcode), 409
