import psycopg2

from data_model.teachers_for_subjects import TeachersForSubjects
from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/teacher_for_subjects", methods=["GET"])
def get_teacher_for_subjects():
    return jsonify([i.__dict__() for i in TeachersForSubjects.get_all(dbf.get_db_source())])


@app.route("/api/v1/teacher_for_subjects/<object_id>", methods=["GET"])
def get_teacher_for_subjects_by_id(object_id):
    return jsonify(TeachersForSubjects.get_by_id(object_id, dbf.get_db_source()).__dict__())


@app.route("/api/v1/teacher_for_subjects", methods=["POST"])
def create_teacher_for_subjects():
    return jsonify(TeachersForSubjects(**request.get_json(), db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()
                   )

@app.route("/api/v1/teacher_for_subjects/<object_id>", methods=["PUT"])
def update_teacher_for_subjects(object_id):
    try:
        TeachersForSubjects.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return jsonify(TeachersForSubjects(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()
            )

@app.route("/api/v1/teacher_for_subjects/<object_id>", methods=["DELETE"])
def delete_teacher_for_subjects(object_id):
    try:
        return jsonify(TeachersForSubjects.get_by_id(object_id, db_source=dbf.get_db_source()).delete().__dict__())
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400


if __name__ == '__main__':
    app.run("127.0.0.1", 9000, debug=True)
