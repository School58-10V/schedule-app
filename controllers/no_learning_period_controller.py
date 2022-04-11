import json
import psycopg2

from flask import Flask, request
from psycopg2 import errorcodes

from data_model.no_learning_period import NoLearningPeriod
from services.db_source_factory import DBFactory

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/no-learning-period", methods=["GET"])
def get_no_learning_period():
    return json.dumps([i.__dict__() for i in NoLearningPeriod.get_all(dbf.get_db_source())], ensure_ascii=False, default=str)


@app.route("/api/v1/no-learning-period/<object_id>", methods=["GET"])
def get_no_learning_period_by_id(object_id):
    return json.dumps(NoLearningPeriod.get_by_id(object_id, dbf.get_db_source()).__dict__(), ensure_ascii=False, default=str)


@app.route("/api/v1/no-learning-period", methods=["POST"])
def create_no_learning_period():
    return NoLearningPeriod(**request.get_json(), db_source=dbf.get_db_source()).save().__dict__()


@app.route("/api/v1/no-learning-period/<object_id>", methods=["PUT"])
def update_no_learning_period(object_id):
    try:
        NoLearningPeriod.get_by_id(object_id, dbf.get_db_source())
    except ValueError:
        return "", 404
    return NoLearningPeriod(**request.get_json(), db_source=dbf.get_db_source(), object_id=object_id).save().__dict__()


@app.route("/api/v1/no-learning-period/<object_id>", methods=["DELETE"])
def delete_no_learning_period(object_id):
    try:
        period = NoLearningPeriod.get_by_id(object_id, dbf.get_db_source())
        period = period.delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        return errorcodes.lookup(e.pgcode), 409
    return period


if __name__ == "__main__":
    app.run()
