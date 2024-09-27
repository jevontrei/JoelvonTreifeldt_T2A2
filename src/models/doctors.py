from init import db, ma
from models.treatments import TreatmentSchema

from marshmallow import fields
from marshmallow.validate import Length, Regexp

class Doctor(db.Model):
    __tablename__ = "doctors"

    # Attributes/columns
    doctor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    # password = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(15))
    specialty = db.Column(db.String(30))
    is_admin = db.Column(db.Boolean, default=False)

    # One-to-many relationship from the doctor's (parent) perspective
    # does this need to be nested? to avoid circular chaos?
    treatments = db.relationship("Treatment", back_populates="doctor")  # Don't cascade-delete; patients should retain treatment records


class DoctorSchema(ma.Schema):
    # use regex to ...
    email = fields.Email(
        required=True, 
        default_error_messages = {"invalid": "Not a valid email address."}
    )

    # review and understand this deeply
    treatments = fields.Nested(
        TreatmentSchema, 
        many=True, 
        exclude=("doctor_id",)
    )  # the exclude part prevents circular refs

    
    class Meta:
        # need to create a guard clause / error handling for all this validation?
        name = fields.String(validate=Length(100))
        email = fields.String(validate=Length(100))
        # How to do length requirement without breaking seed command? How does the hashing affect this?
        # password = fields.String(validate=Length(50))
        sex = fields.String(validate=Length(15))
        specialty = fields.String(validate=Length(30))
        
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