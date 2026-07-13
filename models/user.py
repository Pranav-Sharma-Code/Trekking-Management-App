from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    treks = db.relationship("Trek", backref="organizer", lazy=True)
    bookings = db.relationship("Booking", backref="participant", lazy=True)