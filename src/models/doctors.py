from init import db, ma
from models.treatments import TreatmentSchema

from marshmallow import fields
from marshmallow.validate import Length#, Regexp

class Doctor(db.Model):
    __tablename__ = "doctors"

    # Attributes/columns
    doctor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    # why bother putthin (100) here when i'm repeating myself below in the schema?
    password = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(15))
    specialty = db.Column(db.String(30))
    is_admin = db.Column(db.Boolean, default=False)

    # One-to-many relationship from the doctor's (parent) perspective
    treatments = db.relationship("Treatment", back_populates="doctor", cascade="all, delete")  # Cascade-delete to maintain database consistency, but this should be improved; patients should retain treatment records


class DoctorSchema(ma.Schema):
    # Validation
    email = fields.Email(
        required=True, 
        default_error_messages = {"invalid": "Not a valid email address."}
    )
    
    password = fields.String(validate=Length(min=8, max=100), load_only=True)

    # Define nested field; Unpack relationship datatype according to foreign schema; each serialised patient output will have a sub-dictionary describing treatment details
    treatments = fields.Nested(
        TreatmentSchema, # should this be in quotes?
        many=True, 
        exclude=("doctor_id",)  # Excluding doctor_id prevents circular references
    )

    # what goes inside and outside of meta class?!
    class Meta:
        # do i need a guard clause / error handling for all this validation?
        name = fields.String(validate=Length(max=100))
        # these should not be inside meta...?
        email = fields.String(validate=Length(max=100))
        # How to do length requirement without breaking seed command? How does the hashing affect this?
        # password = fields.String(validate=Length(max=50))
        sex = fields.String(validate=Length(max=15))
        specialty = fields.String(validate=Length(max=30))
        
        # Tell Marshmallow what to serialise?
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