import psycopg2
from flask import Flask, request, jsonify
from psycopg2 import errorcodes

from data_model.student import Student
from data_model.students_for_groups import StudentsForGroups
from services.db_source_factory import DBFactory

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/student", methods=["GET"])
def get_students():
    result = []
    for student in Student.get_all(dbf.get_db_source()):
        student_data = student.__dict__()
        student_data["groups"] = [group.get_main_id() for group in StudentsForGroups.get_group_by_student_id(student.get_main_id(), dbf.get_db_source())]
        result.append(student_data)
    return jsonify({"students": result})

@app.route("/api/v1/student/get/detailed", methods=["GET"])
def get_students_detailed():
    result = []
    for student in Student.get_all(dbf.get_db_source()):
        student_data = student.__dict__()
        student_data["groups"] = [group.__dict__() for group in
                                  StudentsForGroups.get_group_by_student_id(student.get_main_id(), dbf.get_db_source())]
        result.append(student_data)
    return jsonify({"students": result})

@app.route("/api/v1/student/get/detailed/<object_id>", methods=["GET"])
def get_student_by_id_detailed(object_id):
    try:
        result = Student.get_by_id(object_id, dbf.get_db_source()).__dict__()
        result["groups"] = [group.__dict__() for group in StudentsForGroups.get_group_by_student_id(object_id, dbf.get_db_source())]
    except ValueError:
        return "", 404
    return jsonify(result)



@app.route("/api/v1/student/<object_id>", methods=["GET"])
def get_student_by_id(object_id):
    try:
        result = Student.get_by_id(object_id, dbf.get_db_source()).__dict__()
        result["groups"] = [group_obj.get_main_id() for group_obj in StudentsForGroups.get_group_by_student_id(object_id, dbf.get_db_source())]
    except ValueError:
        return "", 404
    return jsonify(result)



@app.route("/api/v1/student", methods=["POST"])
def create_student():
    try:
        req = request.get_json()
        result = Student(full_name=req["full_name"], date_of_birth=req["date_of_birth"],
                                 contacts=req["contacts"], bio=req["bio"],
                                 db_source=dbf.get_db_source()).save()
        for elem in req["groups"]:
            StudentsForGroups(student_id=result.get_main_id(), group_id=int(elem), db_source=dbf.get_db_source()).save()
        return jsonify(result.__dict__())
    except TypeError as e:
        print(e)
        return "", 400
    except ValueError as e:
        print(e)
        return "", 400


@app.route("/api/v1/student/<object_id>", methods=["PUT"])
def update_student(object_id):
    try:
        Student.get_by_id(object_id, dbf.get_db_source())
        result = Student(**request.get_json(), db_source=dbf.get_db_source(), object_id=object_id).save().__dict__()
        return jsonify(result)
    except ValueError:
        return "", 404
    except TypeError:
        return "", 400


@app.route("/api/v1/student/<object_id>", methods=["DELETE"])
def delete_student(object_id):
    try:
        student = Student.get_by_id(object_id, dbf.get_db_source())
        student = student.delete().__dict__()
        return jsonify(student)
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        return jsonify(errorcodes.lookup(e.pgcode)), 409
      

if __name__ == "__main__":
    app.run()
