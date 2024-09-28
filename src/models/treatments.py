from init import db, ma
from marshmallow import fields

class Treatment(db.Model):
    __tablename__ = "treatments"
    
    # Attributes/columns
    treatment_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)  # End date is optional; treatment may be ongoing
    
    # Foreign keys from parent tables
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)  # Deleting a patient deletes their treatments and therefore appointments
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id", ondelete="CASCADE"), nullable=False)  # Deleting a doctor deletes their treatments to maintain database consistency; but this should be improved. Patients should retain history and agency. Implement this in future: deleting a doctor sets the treatment end_date to yesterday if it hasn't already passed

    # Many-to-one relationships from the treatment's perspective (child)
    patient = db.relationship("Patient", back_populates="treatments")
    doctor = db.relationship("Doctor", back_populates="treatments")
    
    # One-to-many relationship from the treatment's perspective (parent)
    appointments = db.relationship("Appointment", back_populates="treatment", cascade="all, delete")  # Cascade; deleting a treatment deletes all child appointments; but this should be improved; patient should retain history. Treatments should not be deleted, and if they are, an admin should dump the raw appointment data into the patient's log as an archive before deleting

# TO DO: verify that end date is AFTER start date?! do that in schema?

class TreatmentSchema(ma.Schema):
    # remember to constrain each entry to be unique... right now you can create 100+ different identical treatment entries?!
    # remember to validate that end date, if it exists, is on or after start date?!:

    class Meta:
        fields = (
            # this should have patient, not patient_id etc?
            "treatment_id", 
            "patient_id", 
            "doctor_id", 
            "start_date", 
            "end_date"
        )


# Subclass schema for singular and plural cases
treatment_schema = TreatmentSchema()
treatments_schema = TreatmentSchema(many=True)
