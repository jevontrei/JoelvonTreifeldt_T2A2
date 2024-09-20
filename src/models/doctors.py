from init import db, ma
from models.treatments import TreatmentSchema

from marshmallow import fields


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