from init import db
from models.patient import Patient, patient_schema, patients_schema


@app.route("/")
def welcome():
    return "Welcome. Let's get healthy."


@app.route("/patients/")
def get_all_patients():
    stmt = db.select(Patient).order_by(Patient.name)
    patients = db.session.scalar(stmt)
    return patients_schema.dump(patients)
