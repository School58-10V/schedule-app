import json
from data_model.teachers_for_subjects import TeachersForSubjects
from services.db_source_factory import DBFactory
from flask import Flask, request

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/teacher_for_subjects", methods=["GET"])
def get_teacher_for_subjects():
    return json.dumps([i.__dict__() for i in TeachersForSubjects.get_all(dbf.get_db_source())], ensure_ascii=False)


@app.route("/api/v1/teacher_for_subjects/<object_id>", methods=["GET"])
def get_teacher_for_subjects_by_id(object_id):
    return json.dumps(TeachersForSubjects.get_by_id(object_id, dbf.get_db_source()).__dict__(), ensure_ascii=False)


@app.route("/api/v1/teacher_for_subjects", methods=["POST"])
def create_teacher_for_subjects():
    return TeachersForSubjects(**request.get_json(), db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/teacher_for_subjects/<object_id>", methods=["PUT"])
def update_teacher_for_subjects(object_id):
    try:
        TeachersForSubjects.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return TeachersForSubjects(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source()) \
        .save() \
        .__dict__()


@app.route("/api/v1/teacher_for_subjects/<object_id>", methods=["DELETE"])
def delete_teacher_for_subjects(object_id):
    if request.method == 'DELETE':
        return TeachersForSubjects.get_by_id(object_id, db_source=dbf.get_db_source()).delete().__dict__()


if __name__ == '__main__':
    app.run()
