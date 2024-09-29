from init import db, ma
# from models.treatments import TreatmentSchema

from marshmallow import fields
from marshmallow.validate import Length


class Doctor(db.Model):
    __tablename__ = "doctors"

    # Attributes/columns
    doctor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(15))
    specialty = db.Column(db.String(30))
    is_admin = db.Column(db.Boolean, default=False)

    # One-to-many relationship from the doctor's (parent) perspective
    # Cascade-delete to maintain database consistency, but this should be improved; patients should retain treatment records
    treatments = db.relationship(
        "Treatment", back_populates="doctor", cascade="all, delete")


class DoctorSchema(ma.Schema):
    # Validation
    name = fields.String(validate=Length(max=100))
    password = fields.String(validate=Length(min=8, max=100), load_only=True)
    sex = fields.String(validate=Length(max=15))
    specialty = fields.String(validate=Length(max=30))
    is_admin = fields.Boolean()
    
    email = fields.Email(
        required=True,
        validate=Length(max=100),
        default_error_messages={"invalid": "Not a valid email address."}
    )

    # Define nested field; Unpack relationship datatype according to foreign schema; each serialised patient output will have a sub-dictionary describing treatment details
    treatments = fields.Nested(
        "TreatmentSchema",  # This is in quotes to avoid circular references
        many=True,
        # Excluding doctor_id prevents circular references
        exclude=("doctor_id",)
    )

    class Meta:
        # Tell Marshmallow what to serialise
        fields = (
            "doctor_id",
            "name",
            "email",
            "password",
            "sex",
            "specialty",
            "is_admin",
            "treatments"
        )


# Subclass schema for singular and plural cases
doctor_schema = DoctorSchema(exclude=["password"])
doctors_schema = DoctorSchema(many=True, exclude=["password"])
