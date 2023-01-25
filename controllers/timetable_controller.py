from __future__ import annotations

import io
from typing import TYPE_CHECKING

import psycopg2, logging
from flask import request, jsonify

import numpy as np
import pandas as pd
import itertools

from schedule_app import app
from data_model.timetable import TimeTable
from validators.timetable_validator import TimetableValidator

if TYPE_CHECKING:
    from flask import Response
    from typing import Union, Any, Tuple

validator = TimetableValidator()


@app.route("/api/v1/timetable", methods=["GET"])
def get_timetable() -> Response:
    try:
        return jsonify([i.__dict__() for i in TimeTable.get_all(app.config.get("schedule_db_source"))])
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/timetable/<int:object_id>", methods=["GET"])
def get_timetable_by_id(object_id) -> Response:
    try:
        return jsonify(TimeTable.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
    except ValueError:
        return "", 404


@app.route("/api/v1/timetable", methods=["POST"])
def create_timetable() -> Union[Response, Tuple[str, int]]:
    try:
        validator.validate(request.get_json(), "POST")
    except ValueError:
        return "", 400
    try:
        return jsonify(TimeTable(**request.get_json(),
                                 db_source=app.config.get("schedule_db_source")).save().__dict__())
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/timetable/<int:object_id>", methods=["PUT"])
def update_timetable(object_id: int) -> Union[Tuple[str, int], Response]:
    if request.get_json().get('object_id') != object_id:
        return "", 400
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        TimeTable.get_by_id(object_id, db_source=app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        return jsonify(TimeTable(**request.get_json(),
                                 db_source=app.config.get("schedule_db_source")).save().__dict__())
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/timetable/<int:object_id>", methods=["DELETE"])
def delete_timetable(object_id: int) -> Union[Response, Tuple[str, int], Tuple[Any, int]]:
    try:
        timetable = TimeTable.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        timetable = timetable.delete().__dict__()
        return jsonify(timetable)
    except psycopg2.Error as e:
        return jsonify(psycopg2.errorcodes.lookup(e.pgcode)), 409
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


def parse_class_lesson(information):
    return tuple(map(str.strip, information))


def parse_group_lesson(information):
    subject_name = [information[0].strip()]
    teacher_names = [information[1].strip()]
    classrooms = []

    for el in information[2:-1]:
        classroom, *teacher = el.strip().split(' ')

        classrooms.append(classroom)
        teacher_names.append(' '.join(teacher))

    classrooms.append(information[-1].strip())

    subjects = list(itertools.zip_longest(subject_name, teacher_names, classrooms, fillvalue=subject_name[0]))

    return subjects


def tuple_to_dict(keys: list, values: tuple):
    return dict(zip(keys, values))


def check_if_group_lesson(data):
    return type(data) == list


def parse_and_set_lesson(i, j, el, df):
    try:
        np.isnan(el)  # проверяем, пропуск или нет

        if i != 0 and i % 2 == 1:
            df.iloc[i, j] = df.iloc[i - 1, j]
        elif j != 0 and check_if_group_lesson(df.iloc[i, j - 1]):
            df.iloc[i, j] = df.iloc[i, j - 1]

    except TypeError:
        information = el.split(',')

        if len(information) == 3:
            lesson = parse_class_lesson(information)
        else:
            lesson = parse_group_lesson(information)

        df.iloc[i, j] = lesson


def parse_parallel(columns, shift, df):
    for j, col in enumerate(columns, 2 + shift):
        for i, el in enumerate(df[col]):
            parse_and_set_lesson(i, j, el, df)

    return df


def parse_day(df):
    shift = 0
    for parallel in range(7, 11 + 1):
        columns = [col for col in df.columns if str(parallel) in col]
        df = parse_parallel(columns, shift, df)
        shift += len(columns)

    return df


@app.route('/api/v1/timetable/upload', methods=['POST'])
def upload_files():
    data = request.files['file']

    try:
        bytesFile = io.BytesIO()
        data.save(bytesFile)

        xls = pd.ExcelFile(bytesFile)
        sheet_to_df = pd.read_excel(xls, sheet_name=None)
        print(sheet_to_df)
        timetable = {}
        for el in sheet_to_df:
            df = sheet_to_df[el]

            df.columns = df.iloc[0].values
            df.rename(columns={np.nan: 'Время звонков'}, inplace=True)
            df.drop(0, inplace=True)

            df = parse_day(df)

            timetable[el] = df.drop(['Звонки', 'Время звонков'], axis=1).fillna('Нет урока').to_dict()
            timetable['classes'] = df.drop(['Звонки', 'Время звонков'], axis=1).columns.values.tolist()

            print(f'Получили и успешно спарсили расписание на один день с листа {el}')

        return jsonify(timetable), 200
    except Exception as e:
        print(e)
        return '', 500


@app.route('/api/v1/timetable/upload1', methods=['POST']) # просто
def test_func():
    a = request.get_json()
    print(a)
    return '', 200
