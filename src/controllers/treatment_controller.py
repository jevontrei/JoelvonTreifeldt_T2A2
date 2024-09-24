from init import db
from models import Treatment, treatment_schema, treatments_schema, Appointment, appointment_schema, appointments_schema
from utils import authorise_as_admin  # , authorise_as_appt_participant

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

#####################################################

# TO DO: verify that end date is AFTER start date?!

#####################################################

# Create blueprint with URL prefix
treatments_bp = Blueprint(
    "treatments",
    __name__,
    url_prefix="/treatments"
)

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
    
    # Fetch data, deserialise it, store in variable
    body_data = request.get_json()

    # Remember to validate input! Especially FKs
    # Define new instance of Treatment class
    treatment = Treatment(
        patient_id=body_data.get("patient_id"),
        doctor_id=body_data.get("doctor_id"),
        start_date=body_data.get("start_date"),
        end_date=body_data.get("end_date")
    )

    # Add treatment to session and commit changes to database
    db.session.add(treatment)
    db.session.commit()

    # Return treatment object serialised according to the treatment schema
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
        date=body_data.get("date"),
        time=body_data.get("time"),
        place=body_data.get("place"),
        cost=body_data.get("cost"),
        status=body_data.get("status"),

        # validate this! check it exists. with a guard clause?
        treatment_id=body_data.get("treatment_id")
    )

    # Add appointment to session and commit changes to database
    db.session.add(appointment)
    db.session.commit()

    # Return appointment object serialised according to the appointment schema
    return appointment_schema.dump(appointment), 201

    # except IntegrityError?:

#####################################################

# http://localhost:5000/treatments/<int:treatment_id>/appointments/


@treatments_bp.route("/<int:treatment_id>/appointments/")
@jwt_required()
# justify deco choice?!
# @authorise_as_admin
# @authorise_as_appt_participant
def get_treatment_appointments(treatment_id):
    """Get all appointments for a particular treatment relationship

    Args:
        treatment_id (_type_): _description_

    Returns:
        _type_: _description_
    """

    # Create SQLAlchemy query statement:
    # SELECT appointments.appt_id, appointments.date, appointments.time, appointments.place, appointments.cost, appointments.status, appointments.notes, appointments.treatment_id
    # FROM appointments
    # WHERE appointments.treatment_id = :treatment_id_1 ORDER BY appointments.date, appointments.time;
    stmt = db.select(
        Appointment
    ).filter_by(
        treatment_id=treatment_id
    ).order_by(
        Appointment.date, Appointment.time
    )

    appointments = db.session.scalars(stmt).fetchall()

    # Guard clause; return error if no appointments exist
    if not appointments:
        return jsonify(
            {"error": f"No appointments found for treatment {treatment_id}."}
        ), 404

    # Return appointment objects serialised according to the appointments schema
    return appointments_schema.dump(appointments)

#####################################################

# http://localhost:5000/treatments/


@treatments_bp.route("/")
@jwt_required()
# justify why i chose this particular auth decorator
@authorise_as_admin
def get_all_treatments():
    """Get all treatments

    Returns:
        _type_: _description_
    """

    # Create SQLAlchemy query statement:
    # SELECT treatments.treatment_id, treatments.start_date, treatments.end_date, treatments.patient_id, treatments.doctor_id
    # FROM treatments
    # ORDER BY treatments.start_date;
    stmt = db.select(
        Treatment
    ).order_by(
        Treatment.start_date
    )

    # Execute statement, store in an iterable object(?)
    treatments = db.session.scalars(stmt).fetchall()

    # Guard clause; return error if no treatments exist
    if not treatments:
        return jsonify(
            {"error": "No treatments found."}
        ), 404

    # Return treatment objects serialised according to the treatments schema
    return treatments_schema.dump(treatments)

#####################################################

# http://localhost:5000/treatments/<int:treatment_id>


@treatments_bp.route("/<int:treatment_id>")
@jwt_required()
# justify why i chose this particular auth decorator
@authorise_as_admin
def get_a_treatment(treatment_id):
    """Get a specific treatment using the id

    Args:
        treatment_id (_type_): _description_

    Returns:
        _type_: _description_
    """

    # Create SQLAlchemy query statement:
    # SELECT treatments.treatment_id, treatments.start_date, treatments.end_date, treatments.patient_id, treatments.doctor_id
    # FROM treatments
    # WHERE treatments.treatment_id = :treatment_id_1;
    stmt = db.select(
        Treatment
    ).filter_by(
        treatment_id=treatment_id
    )

    # Connect to database session, execute statement, store resulting value
    treatment = db.session.scalar(stmt)

    # Guard clause; return error if treatment doesn't exist
    if not treatment:
        return jsonify(
            {"error": f"Treatment {treatment_id} not found."}
        ), 404

    # Return treatment object serialised according to the treatment schema
    return treatment_schema.dump(treatment)

#####################################################

# http://localhost:5000/treatments/<int:treatment_id>


@treatments_bp.route("/<int:treatment_id>", methods=["PUT", "PATCH"])
@jwt_required()
# @authorise_as_admin
# justify why i chose this particular auth decorator
# @authorise_as_appt_participant
def update_treatment(treatment_id):
    """_summary_

    Args:
        treatment_id (_type_): _description_

    Returns:
        _type_: _description_
    """

    body_data = request.get_json()

    # Create SQLAlchemy query statement:
    # SELECT treatments.treatment_id, treatments.start_date, treatments.end_date, treatments.patient_id, treatments.doctor_id
    # FROM treatments
    # WHERE treatments.treatment_id = :treatment_id_1;
    stmt = db.select(
        Treatment
    ).filter_by(
        treatment_id=treatment_id
    )

    # Connect to database session, execute statement, store resulting value
    treatment = db.session.scalar(stmt)

    # Guard clause; return error if treatment doesn't exist
    if not treatment:
        return jsonify(
            {"error": f"Treatment {treatment_id} not found."}
        ), 404

    # can i do this more efficiently with kwargs?
    treatment.patient_id = body_data.get("patient_id") or treatment.patient_id
    treatment.doctor_id = body_data.get("doctor_id") or treatment.doctor_id
    treatment.start_date = body_data.get("start_date") or treatment.start_date
    treatment.end_date = body_data.get("end_date") or treatment.end_date

    # Commit updated details to database
    db.session.commit()

    # Return updated treatment object serialised according to the treatment schema
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

    # Create SQLAlchemy query statement:
    # SELECT treatments.treatment_id, treatments.start_date, treatments.end_date, treatments.patient_id, treatments.doctor_id
    # FROM treatments
    # WHERE treatments.treatment_id = :treatment_id_1;
    stmt = db.select(
        Treatment
    ).filter_by(
        treatment_id=treatment_id
    )

    # Connect to database session, execute statement, store resulting value
    treatment = db.session.scalar(stmt)

    # Guard clause; return error if treatment doesn't exist
    if not treatment:
        return jsonify(
            {"error": f"Treatment {treatment_id} not found."}
        ), 404

    # Delete treatment and commit changes to database
    db.session.delete(treatment)
    db.session.commit()

    # Return serialised success message
    return jsonify(
        {"message": f"Treatment {treatment_id} deleted."}
    )
