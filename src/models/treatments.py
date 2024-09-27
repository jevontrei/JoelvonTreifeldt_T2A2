from init import db, ma


class Treatment(db.Model):
    __tablename__ = "treatments"
    
    # Attributes/columns
    treatment_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    
    # Foreign keys from parent tables
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"), nullable=False)

    # Many-to-one relationships from the treatment's perspective
    patient = db.relationship("Patient", back_populates="treatments")  # why don't i have ondelete="CASCADE" here?
    doctor = db.relationship("Doctor", back_populates="treatments")  # why don't i have ondelete="CASCADE" here?
    
    # This relationship allows us to view a treatment's appts... bi-directionally but no need for a line starting with appt_id = ... bc it's not actually a column in the treatments table, and bc treatments is the parent. this is just to establish the two-way connection
    # One-to-many relationship from the treatment's perspective
    appointments = db.relationship("Appointment", back_populates="treatment", cascade="all, delete")


class TreatmentSchema(ma.Schema):
    # remember to constrain each entry to be unique... right now you can create 100+ different identical treatment entries?!
    # remember to validate that end date, if it exists, is on or after start date:

    class Meta:
        fields = (
            "treatment_id", 
            "patient_id", 
            "doctor_id", 
            "start_date", 
            "end_date"
        )


# Subclass schema for singular and plural cases
treatment_schema = TreatmentSchema()
treatments_schema = TreatmentSchema(many=True)
