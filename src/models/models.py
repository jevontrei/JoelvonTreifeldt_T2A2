from init import db, ma

from marshmallow import fields
from marshmallow.validate import OneOf

# rename to patient.py if i move classes etc to their own files

VALID_STATUSES = ("Scheduled", "Completed", "Cancelled")

#########################################

# on delete cascade? also so that flask drop doesn't freak out
treat = db.Table(
    "treat",
    db.Column('treat_id', db.Integer, primary_key=True),
    db.Column(
        "patient_id",
        db.Integer,
        db.ForeignKey("patients.patient_id"),  # or cascade="all, delete"?
        nullable=False
    ),
    db.Column(
        "doc_id",
        db.Integer,
        db.ForeignKey("doctors.doc_id"),  # or cascade="all, delete"?
        nullable=False
    )
)
# treat.columns

# TreatSchema?!?! do i need it?

#########################################


class Patient(db.Model):
    __tablename__ = "patients"

    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(15))
    diagnoses = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)

    logs = db.relationship("Log", back_populates="patient", cascade="all, delete") # or just cascade="delete"?

    doctors = db.relationship("Doctor", secondary=treat,
                              back_populates="patients")
    


class PatientSchema(ma.Schema):
    # email = fields.String(required=True, validate=Regexp(
    #     "^\S+@\S+\.\S+$", error="Invalid email format"))

    class Meta:
        fields = ("patient_id", "name", "email", "password",
                  "dob", "sex", "diagnoses", "is_admin")
        # fields = ("patient_id", "name", "email", "password", "dob", "sex", "diagnoses", "is_admin", "doctor")


patient_schema = PatientSchema(exclude=["password"])
patients_schema = PatientSchema(many=True, exclude=["password"])

#########################################


class Doctor(db.Model):
    __tablename__ = "doctors"

    doc_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    patients = db.relationship(
        "Patient", secondary=treat, back_populates="doctors")


class DoctorSchema(ma.Schema):
    # email = fields.String(required=True, validate=Regexp(
    #     "^\S+@\S+\.\S+$", error="Invalid email format"))

    class Meta:
        fields = ("doc_id", "name", "email", "password")
        # fields = ("doc_id", "name", "email", "password", "patient")


doctor_schema = DoctorSchema(exclude=["password"])
doctors_schema = DoctorSchema(many=True, exclude=["password"])


#########################################


class Appointment(db.Model):
    __tablename__ = "appointments"

    appt_id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.Date, nullable=False)  # change to datetime, and remember to change seed values etc
    place = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)

    treat_id = db.Column(db.Integer, db.ForeignKey(
        "treat.treat_id"), nullable=False)


class AppointmentSchema(ma.Schema):
    status = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = ("appt_id", "datetime", "place", "cost", "status", "treat_id")

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

#########################################

class Log(db.Model):
    __tablename__ = "logs"

    log_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    symptom = db.Column(db.String, nullable=False)
    # duration is a str, not int, to facilitate multiple timescales
    duration = db.Column(db.String)  
    severity = db.Column(db.String)
    
    # FK from patient (1 to many)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    
    patient = db.relationship("Patient", back_populates="logs")
    
class LogSchema(ma.Schema):
    class Meta:
        fields = ("log_id", "date", "symptom", "duration", "severity", "patient_id")

log_schema = LogSchema()
logs_schema = LogSchema(many=True)