from init import db, ma

from datetime import date, time
from marshmallow import fields
from marshmallow.validate import Length

class Log(db.Model):
    __tablename__ = "logs"

    # make sure i allow duplicate dates... so a patient can make multiple logs in one day. but how to prevent stupid identical duplicates?

    # Attributes/columns
    log_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, nullable=False)
    notes = db.Column(db.String(1000), nullable=False)

    # Foreign key from parent
    # ?do i need ondelete here?
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)  # Deleting a patient deletes their logs

    # Many-to-one relationship from the log's perspective (child)
    patient = db.relationship("Patient", back_populates="logs")


class LogSchema(ma.Schema):
    # Validation
    notes = fields.String(validate=Length(max=1000))
    class Meta:
        fields = (
            "log_id",
            "date",
            "notes",
            "patient_id"
        )


# Subclass schema for singular and plural cases
log_schema = LogSchema()
logs_schema = LogSchema(many=True)
