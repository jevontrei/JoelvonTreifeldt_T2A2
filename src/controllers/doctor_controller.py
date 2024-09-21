from init import db
from models import Doctor, doctor_schema, doctors_schema, Appointment, appointments_schema, Treatment, treatments_schema
# prob have to uncomment these (but understand why!?):
# from models.appointments import Appointment, appointments_schema
# from models.treatments import Treatment, treatments_schema
from utils import authorise_as_admin

 
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

##################################################

doctors_bp = Blueprint("doctors", __name__, url_prefix="/doctors")

##################################################

# http://localhost:5000/doctors/
@doctors_bp.route("/")
# @jwt_required()
def get_all_doctors():
    # create SQL statement
    # SELECT * FROM doctors ORDER BY ...?;
    stmt = db.select(Doctor).order_by(Doctor.name)
    print(stmt)

    doctors = db.session.scalars(stmt)
    
    return doctors_schema.dump(doctors)

##################################################

# http://localhost:5000/doctors/<int:doctor_id>
@doctors_bp.route("/<int:doctor_id>")
# @jwt_required()
def get_a_doctor(doctor_id):
    # create SQL statement
    
    # SELECT * FROM doctors WHERE ... = doctor_id?;
    
    stmt = db.select(Doctor).filter_by(doctor_id=doctor_id)
    print(stmt)

    doctor = db.session.scalar(stmt)
    
    # guard clause
    if not doctor:
        return jsonify({"error": f"Doctor {doctor_id} not found."}), 404
    
    return doctor_schema.dump(doctor)

##################################################

@appointments_bp.route("/doctors/<int:doctor_id>")
# @jwt_required()
def get_doctor_appointments(doctor_id):
    """
    Get all appointments for a particular doctor

    Args:
        doctor_id (_type_): _description_

    Returns:
        JSON: a list of appointments for the given doctor
    """
    
    # create SQL statement

    # SELECT appointments.appt_id, appointments.datetime, appointments.place, appointments.cost, appointments.status, appointments.treatment_id 
    # FROM appointments JOIN treatments ON treatments.treatment_id = appointments.treatment_id 
    # WHERE treatments.doctor_id = :doctor_id_1

    stmt = db.select(Appointment).join(Treatment).filter(
        Treatment.doctor_id==doctor_id
        )#.order_by()

    # print(stmt)
    
    # execute SQL statement using scalars()
    # use fetchall() to return scalar values, which avoids returning an empty list for queries for nonexistent doctors (e.g. doctor_id=9999)
    appointments = db.session.scalars(stmt).fetchall()

    # guard clause
    if not appointments:
        return jsonify({"error": f"No appointments found for doctor {doctor_id}."}), 404

    # serialise and return
    return appointments_schema.dump(appointments)

#####################################################

# http://localhost:5000/doctors/<int:doctor_id>/treatments/
@doctors_bp.route("<int:doctor_id>/treatments/")
@jwt_required()
# justify why i chose this particular auth decorator
@authorise_as_admin
def get_doctor_treatments(doctor_id):
    """
    Get all treatment details for a particular doctor

    Args:
        doctor_id (_type_): _description_
    """
    # create SQL statement

    # SELECT treatments.treatment_id, treatments.start_date, treatments.end_date, treatments.patient_id, treatments.doctor_id 
    # FROM treatments 
    # WHERE treatments.doctor_id = :doctor_id_1
    
    stmt = db.select(Treatment).filter_by(doctor_id=doctor_id)#.order_by()
    print(stmt)

    # need to use .fetchall() for scalars plural (write this comment everywhere, and remove fetchall() from any singular ones?!)
    treatments = db.session.scalars(stmt).fetchall()
    
    # guard clause
    if not treatments:
        return jsonify({"error": f"No treatments found for doctor {doctor_id}."}), 404
    
    return treatments_schema.dump(treatments)

##################################################

# http://localhost:5000/doctors/<int:doctor_id>
@doctors_bp.route("/<int:doctor_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_doctor(doctor_id):
    
    body_data = request.get_json()
    
    # create SQL statement
    # SELECT * FROM doctors WHERE ... = doctor_id?;
    stmt = db.select(Doctor).filter_by(doctor_id=doctor_id)
    print(stmt)

    doctor = db.session.scalar(stmt)
    
    # guard clause
    if not doctor:
        return jsonify({"error": f"Doctor {doctor_id} not found."}), 404
    
    doctor.name = body_data.get("name") or doctor.name
    doctor.email = body_data.get("email") or doctor.email
    doctor.password = body_data.get("password") or doctor.password
    # patients and appointments? no, do this through treatments and appointments, respectively?

    db.session.commit()
    
    return doctor_schema.dump(doctor)

##################################################

# http://localhost:5000/doctors/<int:doctor_id>
@doctors_bp.route("/<int:doctor_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_doctor(doctor_id):
    
    # create SQL statement
    
    # SELECT * FROM doctors WHERE doctor_id = doctor_id?;
    
    stmt = db.select(Doctor).filter_by(doctor_id=doctor_id)
    print(stmt)

    doctor = db.session.scalar(stmt)

    # guard clause
    if not doctor:
        return jsonify({"error": f"Doctor {doctor_id} not found."}), 404

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({"message": f"Doctor {doctor_id} deleted."})