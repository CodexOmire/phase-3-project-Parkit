from flask import Blueprint, jsonify, request
from app import db
from models import User

users_bp = Blueprint("users_bp", __name__)

@users_bp.route("/", methods=["GET"])  # GET /users
def list_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@users_bp.route("/", methods=["POST"])  # POST /users
def create_user():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "'name' and 'email' are required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@users_bp.route("/<int:user_id>", methods=["GET"])  # GET /users/<id>
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

@users_bp.route("/<int:user_id>", methods=["PATCH"])  # PATCH /users/<id>
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    if email and User.query.filter(User.email == email, User.id != user_id).first():
        return jsonify({"error": "Email already in use"}), 400
    if name is not None:
        user.name = name
    if email is not None:
        user.email = email
    db.session.commit()
    return jsonify(user.to_dict())

@users_bp.route("/<int:user_id>", methods=["DELETE"])  # DELETE /users/<id>
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.reservations and len(user.reservations) > 0:
        return jsonify({"error": "Cannot delete user with reservations"}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})
