from init import db, ma

from marshmallow import fields
from marshmallow.validate import OneOf

# rename to patient.py if i move classes etc to their own files

VALID_STATUSES = ("Scheduled", "Completed", "Cancelled")

#########################################


class Treatment(db.Model):
    # change this to "treatments" plural and figure out where else to change it!
    __tablename__ = "treatment"
    treatment_id = db.Column(db.Integer, primary_key=True)
    
    # do i need the "patient_id" etc names here?:
    patient_id = db.Column("patient_id", db.Integer, db.ForeignKey(
        "patients.patient_id"), nullable=False)
    doc_id = db.Column("doc_id", db.Integer, db.ForeignKey(
        "doctors.doc_id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    # not sure if these cascade bits should be here... delet?:
    patient = db.relationship("Patient", back_populates="treatment")  # , cascade="all, delete"
    doctor = db.relationship("Doctor", back_populates="treatment")  # , cascade="all, delete"


class TreatmentSchema(ma.Schema):

    # remember to constrain each entry to be unique
    # remember to validate that end date, if it exists, is on or after start date:

    class Meta:
        fields = ("treatment_id", "patient_id", "doc_id", "start_date", "end_date")


treatment_schema = TreatmentSchema()
treatments_schema = TreatmentSchema(many=True)

#########################################


class Patient(db.Model):
    __tablename__ = "patients"

    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(15))
    is_admin = db.Column(db.Boolean, default=False)

    logs = db.relationship(
        "Log", back_populates="patient", cascade="all, delete")

    # check if this makes sense as cascade
    treatment = db.relationship(
        "Treatment", back_populates="patient", cascade="all, delete")


class PatientSchema(ma.Schema):
    # email = fields.String(required=True, validate=Regexp(
    #     "^\S+@\S+\.\S+$", error="Invalid email format"))


    treatment = fields.Nested(TreatmentSchema, many=True)
    class Meta:
        fields = ("patient_id", "name", "email", "password",
                  "dob", "sex", "is_admin", "treatment")


patient_schema = PatientSchema(exclude=["password"])
patients_schema = PatientSchema(many=True, exclude=["password"])

#########################################


class Doctor(db.Model):
    __tablename__ = "doctors"

    doc_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    # check if this makes sense as cascade
    treatment = db.relationship(
        "Treatment", back_populates="doctor", cascade="all, delete")


class DoctorSchema(ma.Schema):
    # email = fields.String(required=True, validate=Regexp(
    #     "^\S+@\S+\.\S+$", error="Invalid email format"))

    class Meta:
        fields = ("doc_id", "name", "email", "password", "treatment")


doctor_schema = DoctorSchema(exclude=["password"])
doctors_schema = DoctorSchema(many=True, exclude=["password"])


#########################################


class Appointment(db.Model):
    __tablename__ = "appointments"

    appt_id = db.Column(db.Integer, primary_key=True)
    # change to datetime, and remember to change seed values etc
    datetime = db.Column(db.Date, nullable=False)
    place = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)

    treatment_id = db.Column(db.Integer, db.ForeignKey(
        "treatment.treatment_id", ondelete="CASCADE"), nullable=False)


class AppointmentSchema(ma.Schema):
    status = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = ("appt_id", "datetime", "place", "cost", "status", "treatment_id")


appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

#########################################


class Log(db.Model):
    __tablename__ = "logs"

    log_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)  # add default of today
    symptom = db.Column(db.String, nullable=False)
    # str, not int, to facilitate multiple timescales
    duration = db.Column(db.String)

    severity = db.Column(db.String)

    # FK from patient (1 to many)
    patient_id = db.Column(db.Integer, db.ForeignKey(
        "patients.patient_id", ondelete="CASCADE"), nullable=False)

    patient = db.relationship("Patient", back_populates="logs")


class LogSchema(ma.Schema):
    class Meta:
        fields = ("log_id", "date", "symptom",
                  "duration", "severity", "patient_id")


log_schema = LogSchema()
logs_schema = LogSchema(many=True)
