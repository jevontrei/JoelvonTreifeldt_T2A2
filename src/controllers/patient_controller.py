from init import db
from models import Patient, patient_schema, patients_schema, Appointment, appointments_schema, Treatment, treatments_schema
# may have to uncomment these (but understand why!?):
# from models.appointments import Appointment, appointments_schema
# from models.treatments import Treatment, treatments_schema
from utils import authorise_as_admin

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

##################################################

# create blueprint with url prefix
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

# http://localhost:5000/patients/<int:patient_id>/appointments/
@patients_bp.route("/<int:patient_id>/appointments/")
@jwt_required()
def get_patient_appointments(patient_id):
    """
    Get all appointments for a particular patient

    Args:
        patient_id (_type_): _description_

    Returns:
        JSON: a list of appointments for the given patient
    """
    
    # create SQL statement

    # SELECT appointments.appt_id, appointments.datetime, appointments.place, appointments.cost, appointments.status, appointments.treatment_id 
    # FROM appointments JOIN treatments ON treatments.treatment_id = appointments.treatment_id 
    # WHERE treatments.patient_id = :patient_id_1
    
    stmt = db.select(Appointment).join(Treatment).filter(
        Treatment.patient_id == patient_id
        )#.order_by()

    # print(stmt)
    
    # execute SQL statement using scalars(), and return a list of scalar values with fetchall()
    appointments = db.session.scalars(stmt).fetchall()
    
    # guard clause
    if not appointments:
        return jsonify({"error": f"No appointments found for patient {patient_id}."}), 404

    # serialise and return
    return appointments_schema.dump(appointments)

#####################################################

# http://localhost:5000/patients/<int:patient_id>/treatments/
@patients_bp.route("/<int:patient_id>/treatments/")
@jwt_required()
# justify why i chose this particular auth decorator
@authorise_as_admin
def get_patient_treatments(patient_id):
    """
    Get all treatment details for a particular patient

    Args:
        patient_id (_type_): _description_
    """
    # create SQL statement

    # SELECT treatments.treatment_id, treatments.start_date, treatments.end_date, treatments.patient_id, treatments.doctor_id 
    # FROM treatments 
    # WHERE treatments.patient_id = :patient_id_1

    stmt = db.select(Treatment).filter_by(patient_id=patient_id)#.order_by()
    
    # need to use .fetchall() for scalars plural (write this comment everywhere, and remove fetchall() from any singular ones?!)
    treatments = db.session.scalars(stmt).fetchall()
    
    # guard clause
    if not treatments:
        return jsonify({"error": f"No treatments found for patient {patient_id}."}), 404
    
    return treatments_schema.dump(treatments)

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
    
    # guard clause
    if not patient:
        return jsonify({"error": f"Patient {patient_id} not found."}), 404
    
    patient.name = body_data.get("name") or patient.name
    patient.email = body_data.get("email") or patient.email
    patient.password = body_data.get("password") or patient.password
    patient.dob = body_data.get("dob") or patient.dob
    patient.sex = body_data.get("sex") or patient.sex
    patient.is_admin = body_data.get("is_admin") or patient.is_admin
    # logs and doctors? no, do this through logs and treatments, respectively?

    db.session.commit()
    return patient_schema.dump(patient)

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
    
    # guard clause
    if not patient:
        return jsonify({"error": f"Patient {patient_id} not found."}), 404
    
    db.session.delete(patient)
    
    db.session.commit()
    
    return jsonify({"message": f"Patient {patient_id} deleted."})
