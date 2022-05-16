from data_model.group import Group
from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify
from validators.group_validator import GroupValidator

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/group", methods=["GET"])
def get_groups():
    return jsonify([i.__dict__() for i in Group.get_all(dbf.get_db_source())])


@app.route("/api/v1/group/<object_id>", methods=["GET"])
def get_group_by_id(object_id):
    return jsonify(Group.get_by_id(object_id, dbf.get_db_source()).__dict__())


@app.route("/api/v1/group", methods=["POST"])
def create_group():
    request_validator = GroupValidator()
    try:
        request_validator.validate(request.get_json(), 'POST')
        return Group(**request.get_json(), db_source=dbf.get_db_source()) \
            .save() \
            .__dict__()
    except ValueError:
        return '', 404


@app.route("/api/v1/group/<object_id>", methods=["PUT"])
def update_groups(object_id):
    group_validator = GroupValidator()
    try:
        group_validator.validate(request.get_json(), 'PUT')
        Group.get_by_id(object_id, db_source=dbf.get_db_source())
        return Group(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source()) \
            .save() \
            .__dict__()
    except ValueError:
        return "", 404


@app.route("/api/v1/group/<object_id>", methods=["DELETE"])
def delete_group(object_id):
    if request.method == 'DELETE':
        return Group.get_by_id(object_id, db_source=dbf.get_db_source()).delete().__dict__()


if __name__ == '__main__':
    app.run()
