from init import db
from models import Appointment, appointment_schema, appointments_schema, Treatment
from utils import authorise_as_admin

from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError


##################################################

# create blueprint with url prefix
appointments_bp = Blueprint("appointments", __name__, url_prefix="/appointments")


##################################################

# http://localhost:5000/appointments/
@appointments_bp.route("/")
# @jwt_required()
def get_all_appointments():
    """_summary_

    Returns:
        _type_: _description_
    """
    
    # create SQL statement
    # SELECT * FROM appointments;
    stmt = db.select(Appointment)  # .order_by(Appointment.datetime)
    
    print(stmt)

    # execute statement
    appointments = db.session.scalars(stmt)
    
    # serialise and return
    return appointments_schema.dump(appointments)


##################################################

# http://localhost:5000/appointments/<int:appt_id>
@appointments_bp.route("/<int:appt_id>")
# @jwt_required()
def get_an_appointment(appt_id):
    """_summary_

    Args:
        appt_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # create SQL statement
    # SELECT * FROM appointments WHERE ... = appt_id?;
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)
    
    print(stmt)
    
    appointment = db.session.scalar(stmt)
    
    # guard clause
    if not appointment:
        return jsonify({
            "error": f"Appointment {appt_id} not found."
            }), 404
    
    return appointment_schema.dump(appointment)


##################################################


@appointments_bp.route("/patients/<int:patient_id>")
# @jwt_required()
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


##################################################


@appointments_bp.route("/", methods=["POST"])
@jwt_required()
def create_appointment():
    # try:
    body_data = request.get_json()
    
    # remember to validate input!
    # define new instance of Appointment class
    appointment = Appointment(
        datetime=body_data.get("datetime"),
        # datetime=body_data["datetime"],  # use this version instead? does it matter?
        
        place=body_data.get("place"),
        # place=body_data["place"],
        
        cost=body_data.get("cost"),
        # cost=body_data["cost"],
        
        status=body_data.get("status"),
        # status=body_data["status"],
        
        # validate this! check it exists. with a guard clause?
        treatment_id=body_data.get("treatment_id")
        # treatment_id=body_data["treatment_id"]
    )
    
    db.session.add(appointment)
    db.session.commit()
    
    return appointment_schema.dump(appointment), 201
    # except IntegrityError?:

##################################################

@appointments_bp.route("/<int:appt_id>", methods=["PUT", "PATCH"])
@jwt_required()
# @authorise_as_admin
# @authorise_as_participant
def update_appointment(appt_id):
    body_data = request.get_json()

    # create SQL statement
    # SELECT * FROM appointments WHERE appointment_id = appointment_id ... ?;
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)
    print(stmt)

    appointment = db.session.scalar(stmt)
    
    # guard clause
    if not appointment:
        return jsonify({"error": f"Appointment {appt_id} not found."}), 404
    
    appointment.datetime = body_data.get("datetime") or appointment.datetime
    appointment.place = body_data.get("place") or appointment.place
    appointment.cost = body_data.get("cost") or appointment.cost
    appointment.status = body_data.get("status") or appointment.status
    db.session.commit()
    
    return appointment_schema.dump(appointment)

##################################################

@appointments_bp.route("/<int:appt_id>", methods=["DELETE"])
@jwt_required()
# @authorise_as_admin
# @authorise_as_participant
def delete_appointment(appt_id):
    # create SQL statement
    
    # SELECT * FROM appointments WHERE ... ?;
    
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)
    print()
    print(stmt)

    appt = db.session.scalar(stmt)
    
    # guard clause
    if not appt:
        return jsonify({"error": f"Appointment {appt_id} not found."}), 404
        
    db.session.delete(appt)
    
    db.session.commit()
    
    return jsonify({"message": f"Appointment {appt_id} deleted."})
