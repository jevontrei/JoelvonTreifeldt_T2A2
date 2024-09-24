from init import db, ma

from marshmallow import fields
from marshmallow.validate import OneOf

VALID_STATUSES = (
    "Scheduled", 
    "Completed", 
    "Cancelled"
)


class Appointment(db.Model):
    __tablename__ = "appointments"

    # Attributes/columns
    appt_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    place = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    notes = db.Column(db.String(1000))

    # Foreign key from parent table
    treatment_id = db.Column(db.Integer, db.ForeignKey("treatments.treatment_id", ondelete="CASCADE"), nullable=False)
    
    # Many-to-one relationship
    treatment = db.relationship("Treatment", back_populates="appointments")


class AppointmentSchema(ma.Schema):
    status = fields.String(
        validate=OneOf(VALID_STATUSES)
    )

    class Meta:
        fields = (
            "appt_id", 
            "date", 
            "time", 
            "place", 
            "cost", 
            "status", 
            "notes", 
            "treatment_id"
        )


# Subclass schema for singular and plural cases
appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)