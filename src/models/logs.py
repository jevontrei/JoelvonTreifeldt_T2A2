from init import db, ma

from datetime import date, datetime
from marshmallow import fields
from marshmallow.validate import Length


class Log(db.Model):
    __tablename__ = "logs"

    # TO-DO: make sure i allow duplicate dates... so a patient can make multiple logs in one day. but remember to prevent identical duplicates

    # Attributes/columns
    log_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, nullable=False)
    time = db.Column(db.Time, default=datetime.now().time())
    notes = db.Column(db.String(1000), nullable=False)

    # Foreign key from parent
    patient_id = db.Column(db.Integer, db.ForeignKey(
        "patients.patient_id", ondelete="CASCADE"), nullable=False)  # Deleting a patient deletes their logs

    # Many-to-one relationship from the log's perspective (child)
    patient = db.relationship("Patient", back_populates="logs")


class LogSchema(ma.Schema):
    # Validation
    date = fields.Date(required=True)
    time = fields.Time()
    notes = fields.String(validate=Length(min=1, max=1000), required=True)
    patient_id = fields.Integer(required=True)

    class Meta:
        # Tell Marshmallow what to serialise
        fields = (
            "log_id",
            "date",
            "time",
            "notes",
            "patient_id"
        )


# Subclass schema for singular and plural cases
log_schema = LogSchema()
logs_schema = LogSchema(many=True)
