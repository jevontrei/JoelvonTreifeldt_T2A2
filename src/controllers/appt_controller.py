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
    
    # Create SQLAlchemy query statement:
    # SELECT appointments.appt_id, appointments.date, appointments.time, appointments.place, appointments.cost, appointments.status, appointments.notes, appointments.treatment_id 
    # FROM appointments 
    # ORDER BY appointments.date, appointments.time;
    stmt = db.select(
        Appointment
    ).order_by(
        Appointment.date, 
        Appointment.time
    )

    # Connect to database session, execute statement, store resulting values; fetchall() prevents returning an empty list/dict
    appointments = db.session.scalars(stmt).fetchall()
    
    # Guard clause: return error if no appointments exist
    if not appointments:
        return jsonify(
            {"error": "No appointments found."}
        ), 404
    
    # Return appointment objects serialised according to the appointments schema 
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

    # Create SQLAlchemy query statement:
    # SELECT appointments.appt_id, appointments.date, appointments.time, appointments.place, appointments.cost, appointments.status, appointments.notes, appointments.treatment_id 
    # FROM appointments 
    # WHERE appointments.appt_id = :appt_id_1;
    stmt = db.select(
        Appointment
    ).filter_by(
        appt_id=appt_id
    )
    
    # Connect to database session, execute statement, store resulting value
    appointment = db.session.scalar(stmt)
    
    # Guard clause; return error if appointment doesn't exist
    if not appointment:
        return jsonify(
            {"error": f"Appointment {appt_id} not found."}
        ), 404
    
    # Return appointment object serialised according to the appointment schema 
    return appointment_schema.dump(appointment)

##################################################

@appointments_bp.route("/<int:appt_id>", methods=["PUT", "PATCH"])
@jwt_required()
# @authorise_as_admin
# @authorise_as_appt_participant
def update_appointment(appt_id):
    """Edit appointment details. User must have a current valid JWT and be an admin (or participant?).

    Args:
        appt_id (int): Appointment primary key.

    Returns:
        JSON: Updated appointment details, serialised according to appointment schema.
    """
    
    # Fetch body of HTTP request
    body_data = request.get_json()

    # Create SQLAlchemy query statement:
    # SELECT appointments.appt_id, appointments.date, appointments.time, appointments.place, appointments.cost, appointments.status, appointments.notes, appointments.treatment_id 
    # FROM appointments 
    # WHERE appointments.appt_id = :appt_id_1;
    stmt = db.select(
        Appointment
    ).filter_by(
        appt_id=appt_id
    )

    # Connect to database session, execute statement, store resulting value
    appointment = db.session.scalar(stmt)
    
    # Guard clause; return error if appointment doesn't exist
    if not appointment:
        return jsonify(
            {"error": f"Appointment {appt_id} not found."}
        ), 404
    
    # Assign updated details to appointment if provided, otherwise use pre-existing defaults
    appointment.date = body_data.get("date", appointment.date)
    appointment.time = body_data.get("time", appointment.time)
    appointment.place = body_data.get("place", appointment.place)
    appointment.cost = body_data.get("cost", appointment.cost)
    appointment.status = body_data.get("status", appointment.status)
    
    # Commit changes to database
    db.session.commit()
    
    # Return updated appointment object serialised according to the appointment schema 
    return appointment_schema.dump(appointment)

##################################################

@appointments_bp.route("/<int:appt_id>", methods=["DELETE"])
@jwt_required()
# @authorise_as_admin
# @authorise_as_appt_participant
def delete_appointment(appt_id):
    """Delete any appointment.

    Args:
        appt_id (int): Appointment primary key.

    Returns:
        JSON: Success message.
    """
    
    # Create SQLAlchemy query statement:
    # SELECT appointments.appt_id, appointments.date, appointments.time, appointments.place, appointments.cost, appointments.status, appointments.notes, appointments.treatment_id 
    # FROM appointments 
    # WHERE appointments.appt_id = :appt_id_1;
    stmt = db.select(
        Appointment
    ).filter_by(
        appt_id=appt_id
    )

    # Connect to database session, execute statement, store resulting value
    appointment = db.session.scalar(stmt)
    
    # Guard clause; return error if no appointment exists
    if not appointment:
        return jsonify(
            {"error": f"Appointment {appt_id} not found."}
        ), 404
        
    # Delete appointment and commit changes to database
    db.session.delete(appointment)
    db.session.commit()
    
    # Return serialised success message
    return jsonify(
        {"message": f"Appointment {appt_id} deleted."}
    )
