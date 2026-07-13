from datetime import datetime
from . import db

class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    trek_id = db.Column( db.Integer, db.ForeignKey("trek.id"), nullable=False)
    booking_date = db.Column( db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="Booked")
    payment_status = db.Column(db.String(20), default="Pending")