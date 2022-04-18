import psycopg2

from data_model.subject import Subject
from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/subjects", methods=["GET"])
def get_subjects():
    return jsonify([i.__dict__() for i in Subject.get_all(dbf.get_db_source())])


@app.route("/api/v1/subjects/<object_id>", methods=["GET"])
def get_subject_by_id(object_id):
    try:
        return jsonify(Subject.get_by_id(object_id, dbf.get_db_source()).__dict__())
    except ValueError:
        return '', 404


@app.route("/api/v1/subjects", methods=["POST"])
def create_subject():
    try:
        return Subject(**request.get_json(), db_source=dbf.get_db_source()).save().__dict__()
    except TypeError:
        return '', 400


@app.route("/api/v1/subjects/<object_id>", methods=["PUT"])
def update_subject(object_id):
    try:
        subject = Subject.get_by_id(object_id, dbf.get_db_source()).__dict__()
        subject.update(request.get_json())
        return jsonify(Subject(**subject, db_source=dbf.get_db_source()).save().__dict__())
    except ValueError:
        return "", 404
    except TypeError:
        return "", 400


@app.route("/api/v1/subjects/<object_id>", methods=["DELETE"])
def delete_subject(object_id):
    try:
        return Subject.get_by_id(object_id, dbf.get_db_source()).delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400


if __name__ == '__main__':
    app.run()
