from init import db, ma

from marshmallow import fields
from marshmallow.validate import OneOf

from datetime import date

# rename to patient.py if i move classes etc to their own files

VALID_STATUSES = ("Scheduled", "Completed", "Cancelled")


#########################################


class Treatment(db.Model):
    __tablename__ = "treatments"
    treatment_id = db.Column(db.Integer, primary_key=True)
    
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    
    patient_id = db.Column(db.Integer, db.ForeignKey(
        "patients.patient_id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey(
        "doctors.doctor_id"), nullable=False)

    # many-to-one
    patient = db.relationship("Patient", back_populates="treatments")
    doctor = db.relationship("Doctor", back_populates="treatments")
    
    # this allows us to view a treatment's appts... bi-directionally but no need for a line starting with appt_id = ... bc it's not actually a column in the treatments table, and bc treatments is the parent. this is just to establish the two-way connection
    # one-to-many
    appointments = db.relationship("Appointment", back_populates="treatment", cascade="all, delete")


class TreatmentSchema(ma.Schema):

    # remember to constrain each entry to be unique
    # remember to validate that end date, if it exists, is on or after start date:

    class Meta:
        fields = ("treatment_id", "patient_id", "doctor_id", "start_date", "end_date")


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

    # one-to-many
    # check if this makes sense as cascade?! i think it does bc this is the parent?
    treatments = db.relationship(
        "Treatment", back_populates="patient", cascade="all, delete")


class PatientSchema(ma.Schema):
    # email = fields.Email(required=True)
    # email = fields.String(required=True, validate=Regexp(
    #     "^\S+@\S+\.\S+$", error="Invalid email format"))

    # review and understand this deeply
    treatments = fields.Nested(TreatmentSchema, many=True, exclude=("patient_id",))  # this exclude part prevents circular refs

    
    class Meta:
        fields = ("patient_id", "name", "email", "password",
                  "dob", "sex", "is_admin", "treatments")


patient_schema = PatientSchema(exclude=["password"])
patients_schema = PatientSchema(many=True, exclude=["password"])


#########################################


class Doctor(db.Model):
    __tablename__ = "doctors"

    doctor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    # does this need to be nested? to avoid circular chaos?
    # check if this makes sense as cascade
    treatments = db.relationship(
        "Treatment", back_populates="doctor", cascade="all, delete")


class DoctorSchema(ma.Schema):
    # email = fields.Email(required=True)
    # email = fields.String(required=True, validate=Regexp(
    #     "^\S+@\S+\.\S+$", error="Invalid email format"))


    # review and understand this deeply
    treatments = fields.Nested(TreatmentSchema, many=True, exclude=("doctor_id",))  # this exclude thing prevents circular refs

    
    class Meta:
        fields = ("doctor_id", "name", "email", "password", "treatments")


doctor_schema = DoctorSchema(exclude=["password"])
doctors_schema = DoctorSchema(many=True, exclude=["password"])


#########################################


class Appointment(db.Model):
    __tablename__ = "appointments"

    appt_id = db.Column(db.Integer, primary_key=True)
    # changed to datetime, and remember to change seed values etc to include time
    datetime = db.Column(db.DateTime, nullable=False)
    place = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    notes = db.Column(db.String(50))

    treatment_id = db.Column(db.Integer, db.ForeignKey(
        "treatments.treatment_id", ondelete="CASCADE"), nullable=False)
    
    treatment = db.relationship("Treatment", back_populates="appointments")


class AppointmentSchema(ma.Schema):
    status = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = ("appt_id", "datetime", "place", "cost", "status", "notes", "treatment_id")


appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)


#########################################


class Log(db.Model):
    __tablename__ = "logs"
    
    # make sure i allow duplicate dates... so a patient can make multiple logs in one day

    log_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, nullable=False)  # is it redundant to use nullable=False AND a default date?
    
    # CHANGE NAME TO NOTES... include word limit?!
    symptom = db.Column(db.String(100), nullable=False)
    
    # str, not int, to facilitate multiple timescales
    # changed symptom to notes, so delete duration and severity
    duration = db.Column(db.String)
    
    # changed symptom to notes, so delete duration and severity
    severity = db.Column(db.String)

    # FK from patient (many-to-one)
    patient_id = db.Column(db.Integer, db.ForeignKey(
        "patients.patient_id", ondelete="CASCADE"), nullable=False)

    # many-to-one?
    patient = db.relationship("Patient", back_populates="logs")


class LogSchema(ma.Schema):
    class Meta:
        fields = ("log_id", "date", "symptom",
                  "duration", "severity", "patient_id")


log_schema = LogSchema()
logs_schema = LogSchema(many=True)
