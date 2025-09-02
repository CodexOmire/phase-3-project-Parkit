from app import db

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, default=True)
    reservations = db.relationship('Reservation', backref='spot', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "available": self.available
        }
