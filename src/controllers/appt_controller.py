# Internal imports
from init import db
from models import Appointment, appointment_schema, appointments_schema, Treatment
from utils import authorise_as_admin

# External imports
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

##################################################

# Create blueprint with URL prefix
appointments_bp = Blueprint(
    "appointments", 
    __name__, 
    url_prefix="/appointments"
)

##################################################

# http://localhost:5000/appointments/
@appointments_bp.route("/")
@jwt_required()
@authorise_as_admin
def get_all_appointments():
    """Get a comprehensive view of all appointments. User must have a current valid JWT and be an admin.

    Returns:
        JSON: All appointment details, serialised according to appointments schema.
    """
    
    # Create SQLAlchemy query statement
    # SELECT appointments.appt_id, appointments.datetime, appointments.place, appointments.cost, appointments.status, appointments.notes, appointments.treatment_id 
    # FROM appointments
    # ORDER BY appointments.datetime;
    stmt = db.select(Appointment).order_by(Appointment.datetime)

    # Connect to database session, execute statement, return resulting values
    appointments = db.session.scalars(stmt)
    
    # do i need a guard clause for if there are no appointments?
    
    # Serialise appointment objects according to the appointments schema and return
    return appointments_schema.dump(appointments)

##################################################

# http://localhost:5000/appointments/<int:appt_id>
@appointments_bp.route("/<int:appt_id>")
@jwt_required()
def get_an_appointment(appt_id):
    """Find any appointment using its unique ID. User must have a current valid JWT and be an admin.

    Args:
        appt_id (int): Appointment primary key.

    Returns:
        JSON: Appointment details, serialised according to appointments schema.
    """

    # Create SQLAlchemy query statement
    # SELECT appointments.appt_id, appointments.datetime, appointments.place, appointments.cost, appointments.status, appointments.notes, appointments.treatment_id 
    # FROM appointments 
    # WHERE appointments.appt_id = :appt_id_1;
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)
    
    # Connect to database session, execute statement, return resulting value
    appointment = db.session.scalar(stmt)
    
    # Guard clause; return error if appointment doesn't exist
    if not appointment:
        return jsonify({
            "error": f"Appointment {appt_id} not found."
            }), 404
    
    # Serialise appointment object according to the appointment schema and return
    return appointment_schema.dump(appointment)

##################################################

@appointments_bp.route("/<int:appt_id>", methods=["PUT", "PATCH"])
@jwt_required()
# @authorise_as_admin
# @authorise_as_participant
def update_appointment(appt_id):
    """Edit appointment details. User must have a current valid JWT and be an admin (or participant?).

    Args:
        appt_id (int): Appointment primary key.

    Returns:
        JSON: Updated appointment details, serialised according to appointment schema.
    """
    
    # Fetch body of HTTP request
    body_data = request.get_json()

    # Create SQLAlchemy query statement
    # SELECT appointments.appt_id, appointments.datetime, appointments.place, appointments.cost, appointments.status, appointments.notes, appointments.treatment_id 
    # FROM appointments 
    # WHERE appointments.appt_id = :appt_id_1;
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)

    # Connect to database session, execute statement, return resulting value
    appointment = db.session.scalar(stmt)
    
    # Guard clause; return error if appointment doesn't exist
    if not appointment:
        return jsonify({"error": f"Appointment {appt_id} not found."}), 404
    
    # Assign updated details to appointment if provided, otherwise use pre-existing defaults
    appointment.datetime = body_data.get("datetime", appointment.datetime)
    appointment.place = body_data.get("place", appointment.place)
    appointment.cost = body_data.get("cost", appointment.cost)
    appointment.status = body_data.get("status", appointment.status)
    
    # Commit changes to database
    db.session.commit()
    
    # Serialise updated appointment object according to appointment schema and return
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
    
    # Create SQLAlchemy query statement
    
    # SELECT * FROM appointments WHERE ... ?
    # ;
    
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)
    print()
    print(stmt)

    appt = db.session.scalar(stmt)
    
    # Guard clause
    if not appt:
        return jsonify({"error": f"Appointment {appt_id} not found."}), 404
        
    db.session.delete(appt)
    
    db.session.commit()
    
    return jsonify({"message": f"Appointment {appt_id} deleted."})
