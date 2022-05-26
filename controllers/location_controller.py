from __future__ import annotations
from typing import TYPE_CHECKING

import logging, psycopg2
from flask import request, jsonify

from schedule_app import app
from data_model.location import Location
from validators.location_validator import LocationValidator

if TYPE_CHECKING:
    from flask import Response
    from typing import Union, Any, Tuple


validator = LocationValidator()


# here will be your code


@app.route("/api/v1/location/<int:object_id>", methods=['PUT'])
def update(object_id: int) -> Union[Tuple[str, int], Response]:
    """
    Обновляем Location
    :param object_id: int
    :return: Response
    """
    if request.get_json().get('object_id') != object_id:
        return "", 400
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        Location.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        return jsonify(Location(**request.get_json(), object_id=object_id,
                                db_source=app.config.get("schedule_db_source")).save().__dict__())
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500



@app.route("/api/v1/location", methods=["GET"])
def get_locations() -> Response | tuple[str, int]:
    """
        Выдаём все Locations
        :return: Response
        """
    try:
        return jsonify([i.__dict__() for i in Location.get_all(app.config.get("schedule_db_source"))])
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500



@app.route("/api/v1/location/<int:object_id>", methods=["GET"])
def get_location_by_id(object_id: int) -> Union[Response, Tuple[str, int]]:
    """
    Выдаём Location по заданному id
    :param object_id: int
    :return: Response
    """
    try:
        return jsonify(Location.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
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
    except ValueError:
        return "", 400
    try:
        return jsonify(Location(**request.get_json(), db_source=app.config.get("schedule_db_source")) \
                       .save().__dict__())
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500




@app.route("/api/v1/location/<int:object_id>", methods=["DELETE"])
def delete_location(object_id: int) -> Union[Tuple[str, int], Tuple[Any, int], Response]:
    """
    Удаляем Location по заданному id
    :param object_id: int
    :return: Response
    """
    try:
        location = Location.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        location = location.delete().__dict__()
    except psycopg2.Error as e:
        return psycopg2.errorcodes.lookup(e.pgcode), 409
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500
    return jsonify(location)
