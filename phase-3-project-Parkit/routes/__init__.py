from flask import Blueprint, jsonify
from models.user import User
from models.spot import ParkingSpot
from models.reservation import Reservation

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify({"message": "Welcome to ParkIt API", "endpoints": ["/spots", "/users", "/reservations"]})

@api.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])

@api.route('/spots')
def get_spots():
    spots = ParkingSpot.query.all()
    return jsonify([{"id": s.id, "name": s.name, "location": s.location, "available": s.available} for s in spots])

@api.route('/reservations')
def get_reservations():
    resvs = Reservation.query.all()
    return jsonify([{
        "id": r.id,
        "user_id": r.user_id,
        "spot_id": r.spot_id,
        "start_time": r.start_time.isoformat(),
        "end_time": r.end_time.isoformat()
    } for r in resvs])
