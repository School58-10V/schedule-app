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
    """
    Достаем все LessonRow
    :return:
    """
    global_dct = {'lesson_rows': []}
    for i in LessonRow.get_all(dbf.get_db_source()):
        local_dct = i.__dict__()
        local_dct['teachers'] = [i.get_main_id() for i in TeachersForLessonRows.
                                 get_teachers_by_lesson_row_id(i.get_main_id(), db_source=dbf.get_db_source())]
        global_dct['lesson_rows'].append(local_dct.copy())

    return jsonify(global_dct)


@app.route('/api/v1/lesson-row/get/detailed')
def get_all_detailed():
    """
    Достаем все LessonRow вместе с учителями
    :return:
    """
    global_dct = {'lesson_rows': []}
    for i in LessonRow.get_all(dbf.get_db_source()):
        local_dct = i.__dict__()
        local_dct['teachers'] = [i.__dict__() for i in TeachersForLessonRows.
                                 get_teachers_by_lesson_row_id(i.get_main_id(), db_source=dbf.get_db_source())]
        global_dct['lesson_rows'].append(local_dct.copy())

    return jsonify(global_dct)

@app.route("/api/v1/lesson-row/<object_id>", methods=["GET"])
def get_lesson_row_by_id(object_id: int):
    """
    Достаем LessonRow по id
    :param object_id: int
    :return:
    """
    try:
        dct = LessonRow.get_by_id(object_id, dbf.get_db_source()).__dict__()
        dct['teachers'] = [i.get_main_id() for i in TeachersForLessonRows.
                           get_teachers_by_lesson_row_id(object_id, db_source=dbf.get_db_source())]
        return jsonify(dct)
    except ValueError:
        return '', 404


@app.route('/api/v1/lesson-row/get/detailed/<object_id>', methods=['GET'])
def get_detailed_lesson_row_by_id(object_id: int):
    """
    Дастаем LessonRow по id вместе с учителями
    :param object_id: int
    :return:
    """
    try:
        dct = LessonRow.get_by_id(object_id, dbf.get_db_source()).__dict__()
        dct['teachers'] = [i.__dict__() for i in TeachersForLessonRows.
                           get_teachers_by_lesson_row_id(object_id, db_source=dbf.get_db_source())]
        return jsonify(dct)
    except ValueError:
        return '', 404


@app.route("/api/v1/lesson-row", methods=["POST"])
def create_lesson_row():
    """
    Создаем LessonRow
    :return:
    """
    return jsonify(LessonRow(**request.get_json(), db_source=dbf.get_db_source()) \
                   .save().__dict__())


@app.route("/api/v1/lesson-row/<object_id>", methods=["PUT"])
def update_lesson_rows(object_id: int):
    """
    Обновляем LessonRow по данному id
    :param object_id:
    :return:
    """
    try:
        LessonRow.get_by_id(object_id, db_source=dbf.get_db_source())
    except ValueError:
        return "", 404
    return jsonify(LessonRow(**request.get_json(), object_id=object_id, db_source=dbf.get_db_source()) \
                   .save().__dict__())


@app.route("/api/v1/lesson-row/<object_id>", methods=["DELETE"])
def delete_lesson_row(object_id: int):
    """
    Удаляем LessonRow по данному id
    :param object_id: int
    :return:
    """
    try:
        lesson_row = LessonRow.get_by_id(object_id, dbf.get_db_source())
        lesson_row = lesson_row.delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        print(e)
        return jsonify(errorcodes.lookup(e.pgcode), 409)
    return jsonify(lesson_row)


if __name__ == '__main__':
    app.run()
