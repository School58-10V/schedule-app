import json
from data_model.location import Location
from services.db_source_factory import DBFactory
from flask import Flask, request

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/location/<object_id>", methods=["DELETE"])
def delete_location(object_id):
    Location.get_by_id(object_id, db_source=dbf.get_db_source()).delete()
    return 'ok', 200


# here will be your code


@app.route("/api/v1/location", methods=["GET"])
def get_groups():
    return json.dumps([i.__dict__() for i in Location.get_all(dbf.get_db_source())], ensure_ascii=False)


@app.route("/api/v1/location/<object_id>", methods=["GET"])
def get_group_by_id(object_id):
    return json.dumps(Location.get_by_id(object_id, dbf.get_db_source()).__dict__(), ensure_ascii=False)


@app.route("/api/v1/location", methods=["POST"])
def create_group():
    return Location(**request.get_json(), db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()

if __name__ == '__main__':
    app.run()
