import psycopg2
from psycopg2 import errorcodes

from data_model.lesson_row import LessonRow
from services.db_source_factory import DBFactory
from flask import Flask, request, jsonify
from data_model.teachers_for_lesson_rows import TeachersForLessonRows

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/lesson-row", methods=["GET"])
def get_all_lesson_rows():
    global_dct = {'lesson_rows': []}
    for i in LessonRow.get_all(dbf.get_db_source()):
        local_dct = i.__dict__()
        local_dct['teachers'] = [i.get_main_id() for i in TeachersForLessonRows.
            get_teachers_by_lesson_row_id(i.get_main_id(), db_source=dbf.get_db_source())]
        global_dct['lesson_rows'].append(local_dct.copy())

    return global_dct


@app.route('/api/v1/lesson-row/get/detailed')
def get_all_detailed():
    global_dct = {'lesson_rows': []}
    for i in LessonRow.get_all(dbf.get_db_source()):
        local_dct = i.__dict__()
        local_dct['teachers'] = [i.__dict__() for i in TeachersForLessonRows.
            get_teachers_by_lesson_row_id(i.get_main_id(), db_source=dbf.get_db_source())]
        global_dct['lesson_rows'].append(local_dct.copy())

    return global_dct


# @app.route("/api/v1/lesson-row/<object_id>", methods=["GET"])
# def get_lesson_row_by_id(object_id):
#     try:
#         return jsonify(LessonRow.get_by_id(object_id, dbf.get_db_source()).__dict__())
#     except ValueError:
#         return '', 404

@app.route("/api/v1/lesson-row/<object_id>", methods=["GET"])
def get_lesson_row_by_id(object_id):
    try:
        dct = LessonRow.get_by_id(object_id, dbf.get_db_source()).__dict__()
        dct['teachers'] = [i.get_main_id() for i in TeachersForLessonRows.
            get_teachers_by_lesson_row_id(object_id, db_source=dbf.get_db_source())]
        return jsonify(dct)
    except ValueError:
        return '', 404


@app.route('/api/v1/lesson-row/get/detailed/<object_id>', methods=['GET'])
def get_detailed_lesson_row_by_id(object_id):
    try:
        dct = LessonRow.get_by_id(object_id, dbf.get_db_source()).__dict__()
        dct['teachers'] = [i.__dict__() for i in TeachersForLessonRows.
            get_teachers_by_lesson_row_id(object_id, db_source=dbf.get_db_source())]
        return jsonify(dct)
    except ValueError:
        return '', 404


@app.route("/api/v1/lesson-row", methods=["POST"])
def create_lesson_row():
    try:
        dct = request.get_json()
        teacher_id = dct.pop('teachers')
        lesson_row = LessonRow(**dct, db_source=dbf.get_db_source()).save()
        for i in teacher_id:
            TeachersForLessonRows(lesson_row_id=lesson_row.get_main_id(), teacher_id=i,
                                  db_source=dbf.get_db_source()).save()
        dct["object_id"] = lesson_row.get_main_id()
        dct['teachers'] = teacher_id
        return jsonify(dct)
    except TypeError:
        return '', 400


@app.route("/api/v1/lesson-row/<object_id>", methods=["PUT"])
def update_lesson_rows(object_id):
    try:
        LessonRow.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    dct = request.get_json()
    new_teachers_id = dct.pop("teachers")
    #
    lesson_row_by_id = LessonRow.get_by_id(object_id, dbf.get_db_source()).__dict__()
    lesson_row_by_id['teachers'] = [i.get_main_id() for i in TeachersForLessonRows.
                                    get_teachers_by_lesson_row_id(object_id, db_source=dbf.get_db_source())]
    old_teachers_id = lesson_row_by_id.pop("teachers")
    for i in range(len(new_teachers_id)):
        tflr = TeachersForLessonRows.get_by_lesson_row_and_teacher_id(teacher_id=old_teachers_id[i],
                                                                      lesson_row_id=object_id,
                                                                      db_source=dbf.get_db_source())


    lesson_row = LessonRow(**dct, object_id=object_id, db_source=dbf.get_db_source()).save().__dict__()
    lesson_row['teachers'] = new_teachers_id
    return lesson_row


@app.route("/api/v1/lesson-row/<object_id>", methods=["DELETE"])
def delete_lesson_row(object_id):
    try:
        lesson_row = LessonRow.get_by_id(object_id, dbf.get_db_source())
        lesson_row = lesson_row.delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        print(e)
        return jsonify(errorcodes.lookup(e.pgcode), 409)
    return jsonify(lesson_row)


@app.route("/api/v1/teacher_for_lesson_rows", methods=["GET"])
def get_teacher_for_lesson_rows():
    return jsonify([i.__dict__() for i in TeachersForLessonRows.get_all(dbf.get_db_source())])


# here will be your code

if __name__ == '__main__':
    app.run()
