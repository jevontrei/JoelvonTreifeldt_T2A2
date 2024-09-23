
from init import db, ma


class Treatment(db.Model):
    __tablename__ = "treatments"
    treatment_id = db.Column(
        db.Integer, 
        primary_key=True
    )
    
    start_date = db.Column(
        db.Date, 
        nullable=False
    )
    end_date = db.Column(db.Date)
    
    patient_id = db.Column(
        db.Integer, 
        db.ForeignKey(
            "patients.patient_id"
        ), 
        nullable=False
    )
    
    doctor_id = db.Column(
        db.Integer, 
        db.ForeignKey(
            "doctors.doctor_id"
        ), 
        nullable=False
    )

    # many-to-one
    patient = db.relationship(
        "Patient", 
        back_populates="treatments"
    )
    doctor = db.relationship(
        "Doctor", 
        back_populates="treatments"
    )
    
    # this allows us to view a treatment's appts... bi-directionally but no need for a line starting with appt_id = ... bc it's not actually a column in the treatments table, and bc treatments is the parent. this is just to establish the two-way connection
    # one-to-many
    appointments = db.relationship(
        "Appointment", 
        back_populates="treatment", 
        cascade="all, delete"
    )


class TreatmentSchema(ma.Schema):

    # remember to constrain each entry to be unique... right now you can create 100 different identical treatment entries?!
    # remember to validate that end date, if it exists, is on or after start date:

    class Meta:
        fields = (
            "treatment_id", 
            "patient_id", 
            "doctor_id", 
            "start_date", 
            "end_date"
        )


treatment_schema = TreatmentSchema()
treatments_schema = TreatmentSchema(many=True)
