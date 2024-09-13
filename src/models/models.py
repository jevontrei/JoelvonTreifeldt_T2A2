from init import db, ma

# rename to patient.py if i move classes etc to their own files

# on delete cascade?
auth = db.Table(
    "auth",
    db.Column('auth_id', db.Integer, primary_key=True),
    db.Column(
        "patient_id",
        db.Integer,
        db.ForeignKey("patients.patient_id"),
        nullable=False
    ),
    db.Column(
        "doc_id",
        db.Integer,
        db.ForeignKey("doctors.doc_id"),
        nullable=False
    )
)
# auth.columns


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

    doctors = db.relationship("Doctor", secondary=auth,
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


class Doctor(db.Model):
    __tablename__ = "doctors"

    doc_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    patients = db.relationship(
        "Patient", secondary=auth, back_populates="doctors")


class DoctorSchema(ma.Schema):
    # email = fields.String(required=True, validate=Regexp(
    #     "^\S+@\S+\.\S+$", error="Invalid email format"))

    class Meta:
        fields = ("doc_id", "name", "email", "password")
        # fields = ("doc_id", "name", "email", "password", "patient")


doctor_schema = DoctorSchema(exclude=["password"])
doctors_schema = DoctorSchema(many=True, exclude=["password"])


class Appointment(db.Model):
    __tablename__ = "appointments"

    appointment_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    place = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)

    auth_id = db.Column(db.Integer, db.ForeignKey(
        "auth.auth_id"), nullable=False)
