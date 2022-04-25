import psycopg2
from data_model.subject import Subject
from data_model.teachers_for_subjects import TeachersForSubjects
from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/subjects", methods=["GET"])
def get_subjects():
    result = []
    for i in Subject.get_all(dbf.get_db_source()):
        subj = i.__dict__()
        subj['teachers'] = [i.__dict__()['object_id'] for i in
                            TeachersForSubjects.get_teachers_by_subject_id(
                                i.get_main_id(), dbf.get_db_source()
                            )]
        result.append(subj)
    return jsonify({'subjects': result})


@app.route("/api/v1/subject/detailed", methods=["GET"])
def get_subjects_detailed():
    result = []
    for i in Subject.get_all(dbf.get_db_source()):
        subj = i.__dict__()
        subj['teachers'] = [i.__dict__() for i in
                            TeachersForSubjects.get_teachers_by_subject_id(
                                i.get_main_id(), dbf.get_db_source()
                            )]
        result.append(subj)
    return jsonify({'subjects': result})


@app.route("/api/v1/subjects/<object_id>", methods=["GET"])
def get_subject_by_id(object_id):
    try:
        return jsonify('teachers', [i.__dict__()['object_id'] for i in
                                    TeachersForSubjects.get_teachers_by_subject_id(object_id, dbf.get_db_source())])
    except ValueError:
        return '', 404


@app.route("/api/v1/subjects", methods=["POST"])
def create_subject():
    try:
        req :dict= request.get_json()
        result = Subject(subject_name=req["subject_name"], db_source=dbf.get_db_source()).save()
        if "teachers" in req.keys():
            for elem in req["teachers"]:
                TeachersForSubjects(subject_id=result.get_main_id(), teacher_id=int(elem), db_source=dbf.get_db_source()).save()
        return jsonify(result.__dict__())
    except TypeError as e:
        print(e)
        return "", 400
    except ValueError as e:
        print(e)
        return "", 400


@app.route("/api/v1/subjects/<object_id>", methods=["PUT"])
def update_subject(object_id):
    try:
        req :dict= request.get_json()
        subject = Subject.get_by_id(object_id, dbf.get_db_source())
        if "teachers" in req.keys():
            for elem in req["teachers"]:
                TeachersForSubjects(subject_id=subject.get_main_id(), teacher_id=int(elem),
                                    db_source=dbf.get_db_source()).save()
        subject.__dict__().update(req)
        return jsonify(Subject(**subject, db_source=dbf.get_db_source()).save().__dict__())
    except ValueError:
        return "", 404
    except TypeError:
        return "", 400


@app.route("/api/v1/subject/detailed/<object_id>", methods=["GET"])
def get_teachers_by_subject_id(object_id):
    try:
        return jsonify('teachers',
                       [i.__dict__() for i in
                        TeachersForSubjects.get_teachers_by_subject_id(object_id, dbf.get_db_source())])
    except ValueError:
        return '', 404


@app.route("/api/v1/subjects/<object_id>", methods=["DELETE"])
def delete_subject(object_id):
    try:
        return Subject.get_by_id(object_id, dbf.get_db_source()).delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.errors.ForeignKeyViolation as error:
        return error.pgerror, 400


if __name__ == '__main__':
    app.run(debug=True)
