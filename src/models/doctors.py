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
    sex = db.Column(db.String(15))
    specialty = db.Column(db.String(30))
    is_admin = db.Column(db.Boolean, default=False)

    # does this need to be nested? to avoid circular chaos?
    # check/TEST if this makes sense as cascade
    # One-to-many relationship from the doctor's perspective
    treatments = db.relationship("Treatment", back_populates="doctor", cascade="all, delete")


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
        name = fields.String(validate=Length(100))
        email = fields.String(validate=Length(100))
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