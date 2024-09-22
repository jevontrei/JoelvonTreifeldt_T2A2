from init import db
from models import Treatment, treatment_schema, treatments_schema, Appointment, appointment_schema, appointments_schema
from utils import authorise_as_admin#, authorise_as_participant

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

#####################################################

# TO DO: verify that end date is AFTER start date?!

#####################################################

# create blueprint with url prefix
treatments_bp = Blueprint("treatments", __name__, url_prefix="/treatments")

#####################################################

# http://localhost:5000/treatments/
@treatments_bp.route("/", methods=["POST"])
@jwt_required()
# must authorise as admin, otherwise any person could create a treatment relationship and view any patient's private logs
@authorise_as_admin
def create_treatment():
    """
    Add a new treatment between doctor and patient

    Args:
        patient_id (_type_): _description_
        doctor_id (_type_): _description_
    """
    # fetch data, deserialise it, store in variable
    body_data = request.get_json()
    
    # remember to validate input! especially FKs
    # define new instance of Treatment class
    treatment = Treatment(
        patient_id=body_data.get("patient_id"),
        doctor_id=body_data.get("doctor_id"),
        start_date=body_data.get("start_date"),
        end_date=body_data.get("end_date")
    )
    
    db.session.add(treatment)
    db.session.commit()

    return treatment_schema.dump(treatment), 201

##################################################

# weird identical duplicates are allowed to happen... fix this?!

# http://localhost:5000/treatments/<int:treatment_id>/appointments/
@treatments_bp.route("/<int:treatment_id>/appointments/", methods=["POST"])
@jwt_required()
def create_appointment(treatment_id):
    """_summary_

    Args:
        treatment_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    # apply integrity error except blox to ALL CREATE FUNCTIONS?!
    
    # try:
    body_data = request.get_json()
    
    # remember to validate input!
    # define new instance of Appointment class
    appointment = Appointment(
        datetime=body_data.get("datetime"),
        # datetime=body_data["datetime"],  # use this version instead? does it matter?
        place=body_data.get("place"),        
        cost=body_data.get("cost"),        
        status=body_data.get("status"),
                
        # validate this! check it exists. with a guard clause?
        treatment_id=body_data.get("treatment_id")
    )
    
    db.session.add(appointment)
    db.session.commit()
    
    return appointment_schema.dump(appointment), 201
    # except IntegrityError?:

#####################################################

# http://localhost:5000/treatments/<int:treatment_id>/appointments/
@treatments_bp.route("/<int:treatment_id>/appointments/")
@jwt_required()
# justify deco choice?!
# @authorise_as_admin
# @authorise_as_participant
def get_treatment_appointments(treatment_id):
    """Get all appointments for a particular treatment relationship

    Args:
        treatment_id (_type_): _description_

    Returns:
        _type_: _description_
    """

    # create SQL statement
    
    # SELECT appointments.appt_id, appointments.datetime, appointments.place, appointments.cost, appointments.status, appointments.notes, appointments.treatment_id 
    # FROM appointments 
    # WHERE appointments.treatment_id = :treatment_id_1;

    stmt = db.select(Appointment).filter_by(treatment_id=treatment_id).order_by(Appointment.datetime)
    print()
    print(stmt)
    
    appointments = db.session.scalars(stmt).fetchall()
    
    if not appointments:
        return jsonify({"error": f"No appointments found for treatment {treatment_id}."}), 404
    
    return appointments_schema.dump(appointments)

#####################################################

# http://localhost:5000/treatments/
@treatments_bp.route("/")
@jwt_required()
# justify why i chose this particular auth decorator
@authorise_as_admin
def get_all_treatments():
    """
    Get all treatments

    Returns:
        _type_: _description_
    """
    # create SQL statement
    
    # SELECT * FROM treatments;
    
    stmt = db.select(Treatment)#.order_by()
    print()
    print(stmt)

    # execute statement, store in an iterable object
    treatments = db.session.scalars(stmt)
    
    # serialise object to JSON, return it
    return treatments_schema.dump(treatments)

#####################################################

# http://localhost:5000/treatments/<int:treatment_id>
@treatments_bp.route("/<int:treatment_id>")
@jwt_required()
# justify why i chose this particular auth decorator
@authorise_as_admin
def get_a_treatment(treatment_id):
    """
    Get a specific treatment using the id

    Args:
        treatment_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # create SQL statement
    
    # SELECT * FROM treatments WHERE treatment_id=treatment_id ... ?;
    
    stmt = db.select(Treatment).filter_by(treatment_id=treatment_id)
    print()
    print(stmt)
    
    treatment = db.session.scalar(stmt)
    
    # guard clause
    if not treatment:
        return jsonify({"error": f"Treatment {treatment_id} not found."}), 404
    
    return treatment_schema.dump(treatment)

#####################################################

# http://localhost:5000/treatments/<int:treatment_id>
@treatments_bp.route("/<int:treatment_id>", methods=["PUT", "PATCH"])
@jwt_required()
# @authorise_as_admin
# justify why i chose this particular auth decorator
# @authorise_as_participant
def update_treatment(treatment_id):
    """_summary_

    Args:
        treatment_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    body_data = request.get_json()
    
    # create SQL statement
    
    # SELECT * FROM treatments WHERE treatment_id = treatment_id ... ?;
    
    stmt = db.select(Treatment).filter_by(treatment_id=treatment_id)
    print()
    print(stmt)
    
    # execute ...
    treatment = db.session.scalar(stmt)
    
    # guard clause
    if not treatment:
        return jsonify({"error": f"Treatment {treatment_id} not found."}), 404
    
    treatment.patient_id = body_data.get("patient_id") or treatment.patient_id
    treatment.doctor_id = body_data.get("doctor_id") or treatment.doctor_id
    treatment.start_date = body_data.get("start_date") or treatment.start_date
    treatment.end_date = body_data.get("end_date") or treatment.end_date

    db.session.commit()
    
    return treatment_schema.dump(treatment)

#####################################################

# http://localhost:5000/treatments/<int:treatment_id>
@treatments_bp.route("/<int:treatment_id>", methods=["DELETE"])
@jwt_required()
# justify why i chose this particular auth decorator
@authorise_as_admin
def delete_treatment(treatment_id):
    """_summary_

    Args:
        treatment_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    # create SQL statement
    
    # SELECT ?;
    
    stmt = db.select(Treatment).filter_by(treatment_id=treatment_id)
    print()
    print(stmt)
    
    # execute statement and ...
    treatment = db.session.scalar(stmt)
    
    # guard clause
    if not treatment:
        return jsonify({"error": f"Treatment {treatment_id} not found."}), 404
        
    db.session.delete(treatment)
    db.session.commit()
    return jsonify({"message": f"Treatment {treatment_id} deleted."})
    