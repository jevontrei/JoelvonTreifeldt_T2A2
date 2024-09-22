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
    stmt = db.select(Appointment)#.order_by(Appointment.datetime)
    print()
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
    """Find an appointment using its unique ID

    Args:
        appt_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    # create SQL statement
    
    # SELECT * FROM appointments WHERE ... = appt_id?;
    
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)
    print()
    print(stmt)
    
    appointment = db.session.scalar(stmt)
    
    # guard clause
    if not appointment:
        return jsonify({
            "error": f"Appointment {appt_id} not found."
            }), 404
    
    return appointment_schema.dump(appointment)

##################################################

@appointments_bp.route("/<int:appt_id>", methods=["PUT", "PATCH"])
@jwt_required()
# @authorise_as_admin
# @authorise_as_participant
def update_appointment(appt_id):
    """_summary_

    Args:
        appt_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    body_data = request.get_json()

    # create SQL statement
    
    # SELECT * FROM appointments WHERE appointment_id = appointment_id ... ?;
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)
    print()
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
    """_summary_

    Args:
        appt_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    
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
