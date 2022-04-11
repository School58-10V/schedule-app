from data_model.teacher import Teacher
from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/teacher", methods=["GET"])
def get_teachers():
    return jsonify([i.__dict__() for i in Teacher.get_all(dbf.get_db_source())])


@app.route("/api/v1/teacher/<object_id>", methods=["GET"])
def get_teacher_by_id(object_id):
    try:
        return jsonify(Teacher.get_by_id(object_id, dbf.get_db_source()).__dict__())
    except:
        return '', 404


@app.route("/api/v1/teacher", methods=["POST"])
def create_teacher():
    return Teacher(**request.get_json(), db_source=dbf.get_db_source()).save().__dict__()


@app.route("/api/v1/teacher/<object_id>", methods=["PUT"])
def update_teacher(object_id):
    try:
        Teacher.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return Teacher(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/teacher/<object_id>", methods=["DELETE"])
def delete_teacher(object_id):
    try:
        Teacher.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return Teacher.get_by_id(object_id, dbf.get_db_source()) \
        .delete() \
        .__dict__()


if __name__ == '__main__':
    app.run()
