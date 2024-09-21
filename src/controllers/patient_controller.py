from init import db
from models import Patient, patient_schema, patients_schema
from utils import authorise_as_admin

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required


##################################################

patients_bp = Blueprint("patients", __name__, url_prefix="/patients")



##################################################

# http://localhost:5000/patients/
@patients_bp.route("/")
# @jwt_required()
def get_all_patients():
    # create SQL statement
    
    # SELECT patients.patient_id, patients.name, patients.email, patients.password, patients.dob, patients.sex, patients.is_admin 
    # FROM patients ORDER BY patients.name
    
    stmt = db.select(Patient).order_by(Patient.name)
    # print(stmt)

    patients = db.session.scalars(stmt)
    return patients_schema.dump(patients)


##################################################

# http://localhost:5000/patients/<int:patient_id>
@patients_bp.route("/<int:patient_id>")
# @jwt_required()
def get_a_patient(patient_id):
    # create SQL statement

    # SELECT patients.patient_id, patients.name, patients.email, patients.password, patients.dob, patients.sex, patients.is_admin 
    # FROM patients 
    # WHERE patients.patient_id = :patient_id_1

    stmt = db.select(Patient).filter_by(patient_id=patient_id)
    # print(stmt)

    patient = db.session.scalar(stmt)
    
    # NEED to prevent empty {} being returned for if not patient!... fetchall()? as well as guard clause? idk. maybe fetchall() doesn't apply for singular scalar
    
    # guard clause
    if not patient:
        return jsonify({"error": f"Patient {patient_id} not found."}), 404
    
    return patient_schema.dump(patient)


##################################################

# http://localhost:5000/patients/<int:patient_id>
@patients_bp.route("/<int:patient_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_patient(patient_id):
    # fetch ...
    body_data = request.get_json()
    
    # create SQL statement
    
    # SELECT patients.patient_id, patients.name, patients.email, patients.password, patients.dob, patients.sex, patients.is_admin 
    # FROM patients 
    # WHERE patients.patient_id = :patient_id_1
    
    stmt = db.select(Patient).filter_by(patient_id=patient_id)
    # print(stmt)

    patient = db.session.scalar(stmt)
    if patient:
        patient.name = body_data.get("name") or patient.name
        patient.email = body_data.get("email") or patient.email
        patient.password = body_data.get("password") or patient.password
        patient.dob = body_data.get("dob") or patient.dob
        patient.sex = body_data.get("sex") or patient.sex
        patient.is_admin = body_data.get("is_admin") or patient.is_admin
        # logs and doctors? no, do this through logs and treatments, respectively?

        db.session.commit()
        return patient_schema.dump(patient)
    else:
        return jsonify({"error": f"Patient {patient_id} not found."}), 404


##################################################

# http://localhost:5000/patients/<int:patient_id>
@patients_bp.route("/<int:patient_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_patient(patient_id):
    
    # create SQL statement

    # SELECT patients.patient_id, patients.name, patients.email, patients.password, patients.dob, patients.sex, patients.is_admin 
    # FROM patients 
    # WHERE patients.patient_id = :patient_id_1

    stmt = db.select(Patient).filter_by(patient_id=patient_id)
    # print(stmt)

    patient = db.session.scalar(stmt)
    
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return jsonify({"message": f"Patient {patient_id} deleted."})  # , 200
    
    else:
        return jsonify({"error": f"Patient {patient_id} not found."}), 404
