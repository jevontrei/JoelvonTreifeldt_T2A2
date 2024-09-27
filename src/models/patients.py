from init import db, ma
from models.treatments import TreatmentSchema

from marshmallow import fields
from marshmallow.validate import Length#, Regexp


class Patient(db.Model):
    __tablename__ = "patients"

    # Attributes/columns
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    # do i need password min/max length? or will the hashing make that freak out?
    password = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(15))
    is_admin = db.Column(db.Boolean, default=False)

    # One-to-many relationships from the patient's (parent) perspective
    logs = db.relationship("Log", back_populates="patient", cascade="all, delete")  # Deleting a patient deletes their logs
    treatments = db.relationship("Treatment", back_populates="patient", cascade="all, delete")  # Deleting a patient deletes their treatments


class PatientSchema(ma.Schema):
    # Validation
    name = fields.String(validate=Length(max=100))
    sex = fields.String(validate=Length(max=15))
    password = fields.String(validate=Length(min=8, max=100), load_only=True)
    
    email = fields.Email(
        required=True, 
        validate=Length(max=100),
        default_error_messages = {"invalid": "Not a valid email address."}
    )

    # Define nested field; each serialised patient output will have a sub-dictionary describing treatment details
    treatments = fields.Nested(
        TreatmentSchema, 
        many=True, 
        exclude=("patient_id",)  # Excluding patient_id prevents circular references
    )
    
    class Meta:
        # do i need a guard clause / error handling for all this validation?
        # Tell Marshmallow what to serialise / how to unpack the patient object / how to do indexing
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

