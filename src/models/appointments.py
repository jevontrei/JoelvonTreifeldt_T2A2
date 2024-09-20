from init import db, ma

from marshmallow import fields
from marshmallow.validate import OneOf

VALID_STATUSES = ("Scheduled", "Completed", "Cancelled")


class Appointment(db.Model):
    __tablename__ = "appointments"

    appt_id = db.Column(db.Integer, primary_key=True)
    # changed to datetime, and remember to change seed values etc to include time
    datetime = db.Column(db.DateTime, nullable=False)
    place = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    notes = db.Column(db.String(50))

    treatment_id = db.Column(db.Integer, db.ForeignKey(
        "treatments.treatment_id", ondelete="CASCADE"), nullable=False)
    
    treatment = db.relationship("Treatment", back_populates="appointments")


class AppointmentSchema(ma.Schema):
    status = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = ("appt_id", "datetime", "place", "cost", "status", "notes", "treatment_id")


appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)