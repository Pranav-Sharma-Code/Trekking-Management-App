from datetime import datetime
from . import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15))
    approved = db.Column(db.Boolean, default=False)
    blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    treks = db.relationship( "Trek",  backref="staff", lazy=True,foreign_keys="Trek.Trek_staff_id")
    bookings = db.relationship("Booking", backref="user", lazy=True, foreign_keys="Booking.participant_id")