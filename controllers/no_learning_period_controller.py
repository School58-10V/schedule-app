import psycopg2
from flask import request, jsonify
from psycopg2 import errorcodes
from validators.no_learning_period_validator import NoLearningPeriodValidator
from services.transformation_services.no_learning_period_transformation_service \
    import NoLearningPeriodTransformationService
from schedule_app import app

transform = NoLearningPeriodTransformationService()
validator = NoLearningPeriodValidator()

@app.route("/api/v1/no-learning-period", methods=["GET"])
def get_no_learning_period():
    return jsonify(transform.get_no_learning_period_transform())


@app.route("/api/v1/no-learning-period/<object_id>", methods=["GET"])
def get_no_learning_period_by_id(object_id):
    try:
        return transform.get_no_learning_period_by_id_transform(object_id)
    except ValueError:
        return "", 404


@app.route("/api/v1/no-learning-period", methods=["POST"])
def create_no_learning_period():
    try:
        validator.validate(request.get_json(), "POST")
        return jsonify(transform.create_no_learning_period_transform(request.get_json()))
    except ValueError:
        return "", 400


@app.route("/api/v1/no-learning-period/<object_id>", methods=["PUT"])
def update_no_learning_period(object_id):
    try:
        validator.validate(request.get_json(), "PUT")
    except ValueError:
        return "", 400
    try:
        return jsonify(transform.update_no_learning_period_transform(object_id, request.get_json()))
    except ValueError:
        return "", 404
    except TypeError:
        return "", 400


@app.route("/api/v1/no-learning-period/<object_id>", methods=["DELETE"])
def delete_no_learning_period(object_id):
    try:
        return jsonify(transform.delete_no_learning_period_transform(object_id))
    except ValueError:
        return "", 404
    except psycopg2.Error as e:
        return jsonify(errorcodes.lookup(e.pgcode)), 409
