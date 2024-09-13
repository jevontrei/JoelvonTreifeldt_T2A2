from init import db
from models.models import Patient, patient_schema, patients_schema
from main import app


@app.route("/patients/")
def get_all_patients():
    stmt = db.select(Patient).order_by(Patient.name)
    patients = db.session.scalars(stmt)
    return patients_schema.dump(patients)
