# seed.py
from app import db
from models.user import User
from models.spot import ParkingSpot
from models.reservation import Reservation

# Drop all tables and create fresh ones (optional)
db.drop_all()
db.create_all()

# Seed Users
users = [
    User(username="alice", email="alice@example.com"),
    User(username="bob", email="bob@example.com")
]
db.session.add_all(users)

# Seed Parking Spots
spots = [
    ParkingSpot(name="CBD Parking", location="Nairobi CBD", available=True),
    ParkingSpot(name="Westlands Lot", location="Westlands", available=False),
    ParkingSpot(name="Karen Mall", location="Karen", available=True)
]
db.session.add_all(spots)

# Seed Reservations
reservations = [
    Reservation(user_id=1, spot_id=2),
    Reservation(user_id=2, spot_id=1)
]
db.session.add_all(reservations)

db.session.commit()
print("Database seeded successfully!")
