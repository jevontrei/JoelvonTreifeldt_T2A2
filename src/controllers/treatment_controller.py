from init import db
from models import Treatment, treatment_schema, treatments_schema, Appointment, appointment_schema, appointments_schema
from utils import authorise_as_admin, authorise_treatment_participant

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

#####################################################

# TO DO: verify that end date is AFTER start date?! do that in schema?

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
# Must authorise as admin, otherwise any person could create a treatment relationship and view any patient's private logs
@authorise_as_admin
def create_treatment():
    """Add a new treatment relationship between doctor and patient.

    Args:
        patient_id (int): Patient primary key.
        doctor_id (int): Doctor primary key.

    Returns:
        tuple: New serialised treatment details (JSON); a 201 HTTP response status code.
    """
    try:
        # need something to check if patient_id and doctor_id exist? --> ForeignKeyViolation

        # Fetch body of HTTP request
        body_data = request.get_json()

        # Abort if empty string is entered for one of the fields; This is necessary because a TypeError except block will not pick up this error
        for field in body_data:
            if body_data[field] == "":
                return jsonify(
                    {"error": f"The {field} is missing or invalid (e.g. empty string)."}
                ), 400

        # Remember to validate input! Especially FKs
        # Define new instance of Treatment class
        treatment = Treatment(
            # Interesting... this works with both int and str input. Why?
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

    # If the provided patient_id or doctor_id cannot be found
    except IntegrityError as e:
        if e.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
            return jsonify(
                {"error": "Foreign key for patient and/or doctor out of range. Ensure those users exist in the database."}
            ), 400

    except DataError as e:
        if e.orig.pgcode == errorcodes.DATETIME_FIELD_OVERFLOW:
            return jsonify(
                # Watch out for other types, not just date
                {"error": f"Invalid date format."}
            ), 400

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500

##################################################

# weird identical duplicates are allowed to happen... fix this?!

# http://localhost:5000/treatments/<int:treatment_id>/appointments/
@treatments_bp.route("/<int:treatment_id>/appointments/", methods=["POST"])
@jwt_required()
# Authorise either patients or their doctors to create appointments, with an early exit for admins
@authorise_treatment_participant
def create_appointment(treatment_id):
    """Create a new appointment for a particular treatment relationship.

    Args:
        treatment_id (int): Treatment primary key.

    Returns:
        tuple: New serialised appointment details (JSON); a 201 HTTP response status code.
    """
    try:
        # Fetch body of HTTP request
        body_data = request.get_json()

        # remember to validate input!
        
        # Define new instance of Appointment class
        appointment = Appointment(
            date=body_data.get("date"),
            time=body_data.get("time"),
            place=body_data.get("place"),
            cost=body_data.get("cost"),
            status=body_data.get("status"),
            treatment_id=body_data.get("treatment_id")
        )

        # Add appointment to session and commit changes to database
        db.session.add(appointment)
        db.session.commit()

        # Return appointment object serialised according to the appointment schema
        return appointment_schema.dump(appointment), 201

    # In case the ?
    except IntegrityError as e:
        return jsonify(
            {"error": f"Treatment ID {treatment_id} not found."}
        ), 404

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


#####################################################

# http://localhost:5000/treatments/<int:treatment_id>/appointments/
@treatments_bp.route("/<int:treatment_id>/appointments/")
@jwt_required()
# Authorise as either a patient or doctor involved in this treatment/appointment, with an early exit for admins
@authorise_treatment_participant
def get_treatment_appointments(treatment_id):
    """Get all appointments for a particular treatment relationship.

    Args:
        treatment_id (int): Treatment primary key.

    Returns:
        JSON: Serialised details of all appointments for a given treatment.
    """
    try:
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

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


#####################################################

# http://localhost:5000/treatments/
@treatments_bp.route("/")
@jwt_required()
# This is a high-level endpoint that should be accessible to admins only
@authorise_as_admin
def get_all_treatments():
    """Get all treatments

    Returns:
        JSON: Serialised treatment details.
    """
    try:
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

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


#####################################################

# http://localhost:5000/treatments/<int:treatment_id>
@treatments_bp.route("/<int:treatment_id>")
@jwt_required()
# Authorise as either a patient or doctor involved in this treatment/appointment, with an early exit for admins
@authorise_treatment_participant
def get_a_treatment(treatment_id):
    """Get details for a specific treatment using its ID.

    Args:
        treatment_id (int): Treatment primary key.

    Returns:
        JSON: Serialised treatment details.
    """
    try:
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

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


#####################################################

# http://localhost:5000/treatments/<int:treatment_id>
@treatments_bp.route("/<int:treatment_id>", methods=["PUT", "PATCH"])
@jwt_required()
# Authorise as either a patient or doctor involved in this treatment/appointment, with an early exit for admins
@authorise_treatment_participant
def update_treatment(treatment_id):
    """Edit treatment details.

    Args:
        treatment_id (int): Treatment primary key.

    Returns:
        JSON: Serialised and updated treatment details.
    """
    try:
        # Fetch body of HTTP request
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
        treatment.patient_id = body_data.get(
            "patient_id") or treatment.patient_id
        treatment.doctor_id = body_data.get("doctor_id") or treatment.doctor_id
        treatment.start_date = body_data.get(
            "start_date") or treatment.start_date
        treatment.end_date = body_data.get("end_date") or treatment.end_date

        # Commit updated details to database
        db.session.commit()

        # Return updated treatment object serialised according to the treatment schema
        return treatment_schema.dump(treatment)

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


#####################################################

# http://localhost:5000/treatments/<int:treatment_id>
@treatments_bp.route("/<int:treatment_id>", methods=["DELETE"])
@jwt_required()
# This is a high-level endpoint that should be accessible to admins only
@authorise_as_admin
def delete_treatment(treatment_id):
    """Delete any treatment. WARNING: Not recommended. This action is destructive and will prevent patients and doctors from viewing ANY appointments associated with this treatment ID. All related appointments will be deleted. The @authorise_treatment_participant decorator will not be functional for appointment GET requests. An admin should archive all related appointment details (especially notes) in the patient's log before deleting treatment.

    Args:
        treatment_id (int): Treatment primary key.

    Returns:
        JSON: Success message.
    """

    try:

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

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500
