import json
from data_model.group import Group
from services.db_source_factory import DBFactory
from flask import Flask, request

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/group", methods=["GET"])
def get_groups():
    return json.dumps([i.__dict__() for i in Group.get_all(dbf.get_db_source())], ensure_ascii=False)


@app.route("/api/v1/group/<object_id>", methods=["GET"])
def get_group_by_id(object_id):
    return json.dumps(Group.get_by_id(object_id, dbf.get_db_source()).__dict__(), ensure_ascii=False)


@app.route("/api/v1/group", methods=["POST"])
def create_group():
    return Group(**request.get_json(), db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/group/<object_id>", methods=["PUT"])
def update_groups(object_id):
    try:
        Group.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return Group(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/group/<object_id>", methods=["DELETE"])
def delete_group(object_id):
    return {"method": "post"}


if __name__ == '__main__':
    app.run()
