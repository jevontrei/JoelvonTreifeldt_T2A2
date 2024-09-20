from init import db, ma

from marshmallow import fields


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

