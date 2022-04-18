import psycopg2

from data_model.teachers_for_subjects import TeachersForSubjects
from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify
from data_model.subject import Subject

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/subject", methods=["GET"])
def get_subjects():
    return jsonify([i.__dict__() for i in Subject.get_all(dbf.get_db_source())])


@app.route("/api/v1/subject/<object_id>", methods=["GET"])
def get_subject_by_id(object_id):
    try:
        return jsonify(Subject.get_by_id(object_id, dbf.get_db_source()).__dict__())
    except ValueError:
        return '', 404


@app.route("/api/v1/subject/<object_id>", methods=["GET"])
def get_teachers_id_by_subject_id(object_id):
    try:
        return jsonify(TeachersForSubjects.get_teachers_by_subject_id(object_id, dbf.get_db_source()))
    except ValueError:
        return '', 404
a

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
    try:
        Subject.get_by_id(object_id, dbf.get_db_source()).delete().__dict__()
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400


if __name__ == '__main__':
    app.run(debug=True)
