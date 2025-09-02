from flask import Blueprint, jsonify, request
from app import db
from models import ParkingSpot

spots_bp = Blueprint("spots_bp", __name__)

@spots_bp.route("/", methods=["GET"])  # GET /spots
def list_spots():
    spots = ParkingSpot.query.all()
    return jsonify([spot.to_dict() for spot in spots])

@spots_bp.route("/", methods=["POST"])  # POST /spots
def create_spot():
    data = request.get_json() or {}
    name = data.get("name")
    location = data.get("location")
    available = data.get("available", True)
    if not name or not location:
        return jsonify({"error": "'name' and 'location' are required"}), 400
    spot = ParkingSpot(name=name, location=location, available=bool(available))
    db.session.add(spot)
    db.session.commit()
    return jsonify(spot.to_dict()), 201

@spots_bp.route("/<int:spot_id>", methods=["GET"])  # GET /spots/<id>
def get_spot(spot_id):
    spot = ParkingSpot.query.get(spot_id)
    if not spot:
        return jsonify({"error": "Spot not found"}), 404
    return jsonify(spot.to_dict())

@spots_bp.route("/<int:spot_id>", methods=["PATCH"])  # PATCH /spots/<id>
def update_spot(spot_id):
    spot = ParkingSpot.query.get(spot_id)
    if not spot:
        return jsonify({"error": "Spot not found"}), 404
    data = request.get_json() or {}
    if "name" in data:
        spot.name = data["name"]
    if "location" in data:
        spot.location = data["location"]
    if "available" in data:
        spot.available = bool(data["available"])  # only manual override when not tied to reservation
    db.session.commit()
    return jsonify(spot.to_dict())

@spots_bp.route("/<int:spot_id>", methods=["DELETE"])  # DELETE /spots/<id>
def delete_spot(spot_id):
    spot = ParkingSpot.query.get(spot_id)
    if not spot:
        return jsonify({"error": "Spot not found"}), 404
    if spot.reservations and len(spot.reservations) > 0:
        return jsonify({"error": "Cannot delete spot with active reservations"}), 400
    db.session.delete(spot)
    db.session.commit()
    return jsonify({"message": "Spot deleted"})
