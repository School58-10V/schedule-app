from data_model.subject import Subject
from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/subject", methods=["GET"])
def get_subjects():
    return jsonify([i.__dict__() for i in Subject.get_all(dbf.get_db_source())], ensure_ascii=False)


@app.route("/api/v1/subject/<object_id>", methods=["GET"])
def get_subject_by_id(object_id):

    try:
        Subject.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return jsonify(Subject.get_by_id(object_id, dbf.get_db_source()).__dict__(), ensure_ascii=False)


@app.route("/api/v1/subject", methods=["POST"])
def create_subject():
    return Subject(**request.get_json(), db_source=dbf.get_db_source()).save().__dict__()


@app.route("/api/v1/subject/<object_id>", methods=["PUT"])
def update_subject(object_id):
    try:
        Subject.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return Subject(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/subject/<object_id>", methods=["DELETE"])
def delete_subject(object_id):
    try:
        Subject.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return Subject.get_by_id(object_id, dbf.get_db_source()) \
        .delete().__dict__()


if __name__ == '__main__':
    app.run(debug=True)
