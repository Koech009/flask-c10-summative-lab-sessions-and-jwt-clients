from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from server.models.workout import Workout
from server.schemas.workout_schema import WorkoutSchema

workouts_bp = Blueprint("workouts", __name__, url_prefix="/api/workouts")

schema = WorkoutSchema()


# CREATE WORKOUT

@workouts_bp.route("/", methods=["POST"])
@jwt_required()
def create_workout():
    try:
        data = request.get_json()
        validated = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user_id = get_jwt_identity()

    workout = Workout(**validated, user_id=user_id)

    db.session.add(workout)
    db.session.commit()

    return schema.dump(workout), 201


# GET ALL WORKOUTS FOR USER with pagination

@workouts_bp.route("/", methods=["GET"])
@jwt_required()
def list_workouts():
    user_id = get_jwt_identity()

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    workouts = (
        Workout.query
        .filter_by(user_id=user_id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return jsonify({
        "workouts": WorkoutSchema(many=True).dump(workouts.items),
        "pagination": {
            "page": workouts.page,
            "per_page": workouts.per_page,
            "total": workouts.total,
            "pages": workouts.pages
        }
    }), 200


# UPDATE WORKOUT
@workouts_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_workout(id):
    user_id = get_jwt_identity()

    workout = Workout.query.filter_by(id=id, user_id=user_id).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    try:
        data = request.get_json()
        validated = schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in validated.items():
        setattr(workout, key, value)

    db.session.commit()

    return schema.dump(workout), 200


# DELETE WORKOUT

@workouts_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_workout(id):
    user_id = get_jwt_identity()

    workout = Workout.query.filter_by(id=id, user_id=user_id).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"msg": "Workout deleted"}), 200
