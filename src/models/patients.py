from init import db, ma
from models.treatments import TreatmentSchema

from marshmallow import fields
from marshmallow.validate import Length, Regexp


class Patient(db.Model):
    __tablename__ = "patients"

    # makr sure these details all match ERD! like char(50) etc

    # Attributes/columns
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(15))
    is_admin = db.Column(db.Boolean, default=False)

    # One-to-many relationships from the patient's (parent) perspective
    logs = db.relationship("Log", back_populates="patient", cascade="all, delete")  # Deleting a patient deletes their logs
    treatments = db.relationship("Treatment", back_populates="patient", cascade="all, delete")  # Deleting a patient deletes their treatments


class PatientSchema(ma.Schema):
    name = fields.String(validate=Length(100))
    sex = fields.String(validate=Length(15))
    
    # how to manage db.String(100) with fields.Email? (one is sqlalchemy, one is marshmallow?)
    # email = fields.String(validate=Length(100))
    # Use regex to ...
    email = fields.Email(
        required=True, 
        default_error_messages = {"invalid": "Not a valid email address."}
    )

    # review and understand this deeply
    treatments = fields.Nested(
        TreatmentSchema, 
        many=True, 
        exclude=("patient_id",)
    )  # the exclude part prevents circular refs

    
    class Meta:
        fields = (
            "patient_id", 
            "name", 
            "email", 
            "password",
            "dob", 
            "sex", 
            "is_admin", 
            "treatments"
        )


# Subclass schema for singular and plural cases
patient_schema = PatientSchema(exclude=["password"])
patients_schema = PatientSchema(many=True, exclude=["password"])

