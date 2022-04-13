from data_model.location import Location
from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import errorcodes

app = Flask(__name__)
dbf = DBFactory()


# here will be your code
@app.route("/api/v1/location/<object_id>", methods=['PUT'])
def update(object_id):
    try:
        Location.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return jsonify(Location(**request.get_json(), object_id=object_id,
                            db_source=dbf.get_db_source()).save().__dict__())


@app.route("/api/v1/location", methods=["GET"])
def get_locations():
    return jsonify([i.__dict__() for i in Location.get_all(dbf.get_db_source())])


@app.route("/api/v1/location/<object_id>", methods=["GET"])
def get_location_by_id(object_id):
    return jsonify(Location.get_by_id(object_id, dbf.get_db_source()).__dict__())


@app.route("/api/v1/location", methods=["POST"])
def create_location():
    return jsonify(Location(**request.get_json(), db_source=dbf.get_db_source()) \
                   .save().__dict__())


@app.route("/api/v1/location/<object_id>", methods=["DELETE"])
def delete_location(object_id):
    try:
        location = Location.get_by_id(object_id, dbf.get_db_source())
        location = location.delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        return errorcodes.lookup(e.pgcode), 409
    return jsonify(location)


if __name__ == '__main__':
    app.run()
