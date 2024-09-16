from init import db
from models.models import Patient, patient_schema, patients_schema
from main import app

##################################################

@app.route("/patients/")
def get_all_patients():
    stmt = db.select(Patient).order_by(Patient.name)
    patients = db.session.scalars(stmt)
    return patients_schema.dump(patients)

##################################################

@app.route("/patients/<int:patient_id>")
def get_a_patient(patient_id):
    stmt = db.select(Patient).filter_by(patient_id=patient_id)
    patient = db.session.scalar(stmt)
    return patient_schema.dump(patient)

##################################################
