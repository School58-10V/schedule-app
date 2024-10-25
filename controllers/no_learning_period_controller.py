import logging, psycopg2

from flask import request, jsonify
from data_model.no_learning_period import NoLearningPeriod
from validators.no_learning_period_validator import NoLearningPeriodValidator
from schedule_app import app


validator = NoLearningPeriodValidator()


@app.route("/api/v1/no-learning-period", methods=["GET"])
def get_no_learning_period():
    try:
        return jsonify([i.__dict__() for i in NoLearningPeriod.get_all(app.config.get("schedule_db_source"))])
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/no-learning-period/<int:object_id>", methods=["GET"])
def get_no_learning_period_by_id(object_id: int):
    try:
        result = jsonify(NoLearningPeriod.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
        return result
    except ValueError:
        return "", 404


@app.route("/api/v1/no-learning-period", methods=["POST"])
def create_no_learning_period():
    validation_data = validator.validate(request.get_json(), "POST")
    if not validation_data[0]:
        return validation_data[1], 400
    try:
        return jsonify(
            NoLearningPeriod(**request.get_json(), db_source=app.config.get("schedule_db_source")).save().__dict__())
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/no-learning-period/<int:object_id>", methods=["PUT"])
def update_no_learning_period(object_id: int):
    if request.get_json().get('object_id') != object_id:
        return "", 400
    validation_data = validator.validate(request.get_json(), "PUT")
    if not validation_data[0]:
        return validation_data[1], 400
    try:
        NoLearningPeriod.get_by_id(object_id, app.config.get("schedule_db_source"))
        result = NoLearningPeriod(**request.get_json(),
                                  db_source=app.config.get("schedule_db_source")).save().__dict__()
        return jsonify(result)
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500


@app.route("/api/v1/no-learning-period/<int:object_id>", methods=["DELETE"])
def delete_no_learning_period(object_id: int):
    try:
        period = NoLearningPeriod.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        return "", 404
    try:
        period = period.delete().__dict__()
    except psycopg2.Error as e:
        return jsonify(psycopg2.errorcodes.lookup(e.pgcode)), 409
    except Exception as err:
        logging.error(err, exc_info=True)
        return "", 500
    return jsonify(period)
