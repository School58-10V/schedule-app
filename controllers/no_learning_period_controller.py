import psycopg2
from flask import Flask, request, jsonify
from psycopg2 import errorcodes

from data_model.no_learning_period import NoLearningPeriod
from validators.no_learning_period_validator import NoLearningPeriodValidator
from services.db_source_factory import DBFactory

app = Flask(__name__)
dbf = DBFactory()


@app.route("/api/v1/no-learning-period", methods=["GET"])
def get_no_learning_period():
    return jsonify([i.__dict__() for i in NoLearningPeriod.get_all(dbf.get_db_source())], ensure_ascii=False, default=str)


@app.route("/api/v1/no-learning-period/<object_id>", methods=["GET"])
def get_no_learning_period_by_id(object_id):
    try:
        result = jsonify(NoLearningPeriod.get_by_id(object_id, dbf.get_db_source()).__dict__())
        return result
    except ValueError:
        return "", 404


@app.route("/api/v1/no-learning-period", methods=["POST"])
def create_no_learning_period():
    request_validator = NoLearningPeriodValidator()
    try:
        request_validator.validate(request.get_json(), 'POST')
        return jsonify(NoLearningPeriod(**request.get_json(), db_source=dbf.get_db_source()).save().__dict__())
    except TypeError:
        return "", 400

      
@app.route("/api/v1/no-learning-period/<object_id>", methods=["PUT"])
def update_no_learning_period(object_id):
    request_validator = NoLearningPeriodValidator()
    try:
        request_validator.validate(request.get_json(), 'PUT')
        NoLearningPeriod.get_by_id(object_id, dbf.get_db_source())
        return jsonify(NoLearningPeriod(**request.get_json(), db_source=dbf.get_db_source(),
                                        object_id=object_id).save().__dict__())
    except ValueError:
        return "", 404
    except TypeError:
        return "", 400


@app.route("/api/v1/no-learning-period/<object_id>", methods=["DELETE"])
def delete_no_learning_period(object_id):
    try:
        period = NoLearningPeriod.get_by_id(object_id, dbf.get_db_source())
        period = period.delete().__dict__()
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        return jsonify(errorcodes.lookup(e.pgcode)), 409
    return jsonify(period)


if __name__ == "__main__":
    app.run()
