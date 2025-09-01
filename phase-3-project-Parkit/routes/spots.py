from flask import Blueprint, jsonify
from models import ParkingSpot

spots_bp = Blueprint("spots_bp", __name__)

@spots_bp.route("/", methods=["GET"])
def get_spots():
    spots = ParkingSpot.query.all()
    return jsonify([spot.to_dict() for spot in spots])
