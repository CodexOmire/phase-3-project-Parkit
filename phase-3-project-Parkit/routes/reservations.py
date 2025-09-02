from flask import Blueprint, jsonify, request
from app import db
from models import Reservation, User, ParkingSpot

reservations_bp = Blueprint("reservations_bp", __name__)

@reservations_bp.route("/", methods=["GET"])  # GET /reservations
def list_reservations():
    reservations = Reservation.query.all()
    return jsonify([r.to_dict() for r in reservations])

@reservations_bp.route("/", methods=["POST"])  # POST /reservations
def create_reservation():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    spot_id = data.get("spot_id")
    if not user_id or not spot_id:
        return jsonify({"error": "'user_id' and 'spot_id' are required"}), 400
    user = User.query.get(user_id)
    spot = ParkingSpot.query.get(spot_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if not spot:
        return jsonify({"error": "Spot not found"}), 404
    if not spot.available:
        return jsonify({"error": "Spot is not available"}), 400
    reservation = Reservation(user_id=user.id, spot_id=spot.id)
    db.session.add(reservation)
    # mark spot unavailable
    spot.available = False
    db.session.commit()
    return jsonify(reservation.to_dict()), 201

@reservations_bp.route("/<int:reservation_id>", methods=["GET"])  # GET /reservations/<id>
def get_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404
    return jsonify(reservation.to_dict())

@reservations_bp.route("/<int:reservation_id>", methods=["PATCH"])  # PATCH /reservations/<id>
def update_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404
    data = request.get_json() or {}
    # For simplicity allow only end_time update (ISO8601 string)
    end_time_str = data.get("end_time")
    if end_time_str:
        from datetime import datetime
        try:
            reservation.end_time = datetime.fromisoformat(end_time_str)
        except Exception:
            return jsonify({"error": "Invalid end_time format"}), 400
    db.session.commit()
    return jsonify(reservation.to_dict())

@reservations_bp.route("/<int:reservation_id>", methods=["DELETE"])  # DELETE /reservations/<id>
def delete_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404
    spot = ParkingSpot.query.get(reservation.spot_id)
    db.session.delete(reservation)
    # free the spot
    if spot:
        spot.available = True
    db.session.commit()
    return jsonify({"message": "Reservation deleted"})
