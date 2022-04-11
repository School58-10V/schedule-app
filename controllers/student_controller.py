from flask import Flask, request, jsonify
from services.db_source_factory import DBFactory
import psycopg2
from data_model.student import Student
from psycopg2 import errorcodes

app = Flask(__name__)
dbf = DBFactory()

@app.route("/api/v1/student", methods=["GET"])
def get_students():
    return jsonify([i.__dict__() for i in Student.get_all(dbf.get_db_source())])

@app.route("/api/v1/student/<object_id>", methods=["GET"])
def get_student_by_id(object_id):
    try:
        result = jsonify(Student.get_by_id(object_id, dbf.get_db_source()).__dict__())
        return result
    except ValueError:
        return "", 404

@app.route("/api/v1/student", methods=["POST"])
def create_student():
    return Student(**request.get_json(), db_source=dbf.get_db_source()).save().__dict__()

@app.route("/api/v1/student/<object_id>", methods=["PUT"])
def update_student(object_id):
    try:
        Student.get_by_id(object_id, dbf.get_db_source())
    except ValueError:
        return "", 404
    return Student(**request.get_json(), db_source=dbf.get_db_source(), object_id=object_id).save().__dict__()

@app.route("/api/v1/student/<object_id>", methods=["DELETE"])
def delete_student(object_id):
    try:
        student = Student.get_by_id(object_id, dbf.get_db_source())
        student = student.delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        return errorcodes.lookup(e.pgcode), 409
    return student

if __name__ == "__main__":
    app.run()
