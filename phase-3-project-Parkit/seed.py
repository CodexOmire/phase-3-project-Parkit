from db import db
from models.user import User
from models.spot import ParkingSpot
from models.reservation import Reservation


def seed_data(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = [
            User(name="alice", email="alice@example.com"),
            User(name="bob", email="bob@example.com")
        ]
        db.session.add_all(users)

        spots = [
            ParkingSpot(name="CBD Parking", location="Nairobi CBD", available=True),
            ParkingSpot(name="Westlands Lot", location="Westlands", available=False),
            ParkingSpot(name="Karen Mall", location="Karen", available=True)
        ]
        db.session.add_all(spots)

        reservations = [
            Reservation(user_id=1, spot_id=2),
            Reservation(user_id=2, spot_id=1)
        ]
        db.session.add_all(reservations)

        # reflect spot availability for seeded reservations
        for r in reservations:
            s = ParkingSpot.query.get(r.spot_id)
            if s:
                s.available = False

        db.session.commit()
        print("Database seeded successfully!")
