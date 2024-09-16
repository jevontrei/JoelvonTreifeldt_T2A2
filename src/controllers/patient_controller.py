from init import db
from models.models import Patient, patient_schema, patients_schema
from main import app
from flask import request

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


@app.route("/patients/", methods=["POST"])
def create_patient():
    body_data = request.get_json()
    # stmt = db.select(Patient)
    # patient = db.session.scalar(stmt)
    # remember to validate input!
    patient = Patient(
        name=body_data.get("name"),
        email=body_data.get("email"),
        password=body_data.get("password"),
        dob=body_data.get("dob"),
        sex=body_data.get("sex"),
        diagnoses=body_data.get("diagnoses"),
        is_admin=body_data.get("is_admin"),
    )

    db.session.add(patient)
    db.session.commit()

    return patient_schema.dump(patient), 201

##################################################


@app.route("/patients/<int:patient_id>", methods=["PUT", "PATCH"])
def update_patient(patient_id):
    body_data = request.get_json()
    stmt = db.select(Patient).filter_by(patient_id=patient_id)
    patient = db.session.scalar(stmt)
    if patient:
        patient.name=body_data.get("name") or patient.name
        patient.email=body_data.get("email") or patient.email
        patient.password=body_data.get("password") or patient.password
        patient.dob=body_data.get("dob") or patient.dob
        patient.sex=body_data.get("sex") or patient.sex
        patient.diagnoses=body_data.get("diagnoses") or patient.diagnoses
        patient.is_admin=body_data.get("is_admin") or patient.is_admin
        # logs and doctors? no, do this through logs and auth, respectively?
        
        db.session.commit()
        return patient_schema.dump(patient)
    else:
        return {"error": f"Patient {patient_id} not found."}  # , 404

##################################################


# DELET A PATIENT
# CASCADE

##################################################
