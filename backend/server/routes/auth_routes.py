from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app import db
from server.models.user import User
from server.schemas.user_schema import UserSchema

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"errors": ["Username and password are required"]}), 400

    if data.get("password") != data.get("password_confirmation"):
        return jsonify({"errors": ["Passwords do not match"]}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"errors": ["Username already exists"]}), 400

    new_user = User(username=data["username"])
    new_user.password = data["password"]
    db.session.add(new_user)
    db.session.commit()

    token = create_access_token(identity=new_user.id)
    return jsonify({"token": token, "user": UserSchema().dump(new_user)}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"errors": ["Username and password are required"]}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.authenticate(data["password"]):
        return jsonify({"errors": ["Invalid username or password"]}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"token": token, "user": UserSchema().dump(user)}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"errors": ["User not found"]}), 404

    return UserSchema().dump(user), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Logged out successfully"}), 200
