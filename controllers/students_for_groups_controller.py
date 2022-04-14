import psycopg2

from flask import Flask, request, jsonify
from psycopg2 import errorcodes

from data_model.students_for_groups import StudentsForGroups
from services.db_source_factory import DBFactory

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/students-for-groups", methods=["GET"])
def get_students_for_groups():
    return jsonify([i.__dict__() for i in StudentsForGroups.get_all(dbf.get_db_source())])


@app.route("/api/v1/students-for-groups/<object_id>", methods=["GET"])
def get_students_for_groups_by_id(object_id):
    try:
        return jsonify(StudentsForGroups.get_by_id(object_id, dbf.get_db_source()).__dict__())
    except ValueError:
        return jsonify(""), 404


@app.route("/api/v1/students-for-groups", methods=["POST"])
def create_students_for_groups():
    try:
        result = jsonify(StudentsForGroups(**request.get_json(), db_source=dbf.get_db_source()).save().__dict__())
        return result
    except TypeError:
        return jsonify(""), 400


@app.route("/api/v1/students-for-groups/<object_id>", methods=["PUT"])
def update_students_for_groups(object_id):
    try:
        StudentsForGroups.get_by_id(object_id, dbf.get_db_source())
        result = StudentsForGroups(**request.get_json(), db_source=dbf.get_db_source(), object_id=object_id).save().__dict__()
        return jsonify(result)
    except ValueError:
        return jsonify(""), 404
    except TypeError:
        return jsonify(""), 400


@app.route("/api/v1/students-for-groups/<object_id>", methods=["DELETE"])
def delete_students_for_groups(object_id):
    try:
        sfg = StudentsForGroups.get_by_id(object_id, dbf.get_db_source())
        sfg = sfg.delete().__dict__()
    except ValueError:
        return jsonify(""), 404
    except psycopg2.Error as e:
        return jsonify(errorcodes.lookup(e.pgcode)), 409
    return jsonify(sfg)


if __name__ == "__main__":
    app.run()
