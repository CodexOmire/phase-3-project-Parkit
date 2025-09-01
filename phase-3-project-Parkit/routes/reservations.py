from flask import Blueprint, jsonify
from models import Reservation

reservations_bp = Blueprint("reservations_bp", __name__)

@reservations_bp.route("/", methods=["GET"])
def get_reservations():
    reservations = Reservation.query.all()
    return jsonify([r.to_dict() for r in reservations])
