import logging, psycopg2

from flask import request, jsonify
from data_model.no_learning_period import NoLearningPeriod
from validators.no_learning_period_validator import NoLearningPeriodValidator
from schedule_app import app
from services.logger.messages_templates import MessagesTemplates


validator = NoLearningPeriodValidator()

LOGGER = logging.getLogger("main.controller")
MESSAGES = MessagesTemplates()
MODEL = "NoLearningPeriod"

@app.route("/api/v1/no-learning-period", methods=["GET"])
def get_no_learning_period():
    try:
        data = [i.__dict__() for i in NoLearningPeriod.get_all(app.config.get("schedule_db_source"))]
        LOGGER.info(MESSAGES.Controller.Success.get_collect_all_message(MODEL))
        return jsonify(data)
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_collect_all(MODEL))
        LOGGER.exception(err)
        return "", 500


@app.route("/api/v1/no-learning-period/<int:object_id>", methods=["GET"])
def get_no_learning_period_by_id(object_id: int):
    try:
        result = jsonify(NoLearningPeriod.get_by_id(object_id, app.config.get("schedule_db_source")).__dict__())
        LOGGER.info(MESSAGES.Controller.Success.get_find_by_id_message(MODEL, object_id))
        return result
    except ValueError:
        LOGGER.error(MESSAGES.Controller.Error.get_find_by_id_message(MODEL))
        return "", 404


@app.route("/api/v1/no-learning-period", methods=["POST"])
def create_no_learning_period():
    validation_data = validator.validate(request.get_json(), "POST")
    if not validation_data[0]:
        LOGGER.error(MESSAGES.General.get_validation_error_message(validation_data[1]))
        return validation_data[1], 400
    try:
        data = NoLearningPeriod(**request.get_json(), db_source=app.config.get("schedule_db_source")).save().__dict__()
        LOGGER.info(MESSAGES.Controller.Success.get_create_message(MODEL))
        return jsonify(data)
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_create_message(MODEL))
        LOGGER.exception(err)
        return "", 500


@app.route("/api/v1/no-learning-period/<int:object_id>", methods=["PUT"])
def update_no_learning_period(object_id: int):
    if request.get_json().get('object_id') != object_id:
        LOGGER.error(MESSAGES.General.get_object_id_mismatch_message())
        return "", 400
    validation_data = validator.validate(request.get_json(), "PUT")
    if not validation_data[0]:
        LOGGER.error(MESSAGES.General.get_validation_error_message(validation_data[1]))
        return validation_data[1], 400
    try:
        NoLearningPeriod.get_by_id(object_id, app.config.get("schedule_db_source"))
        result = NoLearningPeriod(**request.get_json(),
                                  db_source=app.config.get("schedule_db_source")).save().__dict__()
        LOGGER.info(MESSAGES.Controller.Success.get_update_message(MODEL))
        return jsonify(result)
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_update_message(MODEL))
        LOGGER.exception(err)
        return "", 500


@app.route("/api/v1/no-learning-period/<int:object_id>", methods=["DELETE"])
def delete_no_learning_period(object_id: int):
    try:
        period = NoLearningPeriod.get_by_id(object_id, app.config.get("schedule_db_source"))
    except ValueError:
        LOGGER.error(MESSAGES.General.get_id_not_found_message(MODEL, object_id))
        return "", 404
    try:
        period = period.delete().__dict__()
    except psycopg2.Error as e:
        LOGGER.error(MESSAGES.Controller.DBError.get_delete_message(MODEL, psycopg2.errorcodes.lookup(e.pgcode)))
        LOGGER.exception(e)
        return jsonify(psycopg2.errorcodes.lookup(e.pgcode)), 409
    except Exception as err:
        LOGGER.error(MESSAGES.Controller.Error.get_delete_message(MODEL))
        LOGGER.exception(err)
        return "", 500
    LOGGER.info(MESSAGES.Controller.Success.get_delete_message(MODEL))
    return jsonify(period)
