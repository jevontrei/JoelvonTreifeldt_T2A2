from sqlalchemy.exc import IntegrityError
from init import db
from models import Log, log_schema, logs_schema
# , authorise_treatment_participant?
from utils import authorise_as_log_viewer, authorise_as_log_owner, authorise_as_admin

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from datetime import date

############################################

# Create blueprint with URL prefix
# all logs (child) are located under the patient (parent) resource
logs_bp = Blueprint(
    "logs",
    __name__,
    url_prefix="/patients/<int:patient_id>/logs"
)

############################################

# http://localhost:5000/patients/<int:patient_id>/logs/


@logs_bp.route("/", methods=["POST"])
@jwt_required()
# Not even admins can create a log on the patient's behalf. In future, make this possible to increase accessibility
def create_log(patient_id):
    """Create a new patient log.

    Args:
        patient_id (int): Patient primary key.

    Returns:
        tuple: New patient's details, serialised (JSON); a 201 HTTP response status code.
    """
    try:
        # Turn this into a decorator if it gets used in multiple places in future
        # Get the JWT
        jwt = get_jwt()
        # Guard clause; return error if user is not a patient
        if jwt.get("user_type") != "patient":
            return jsonify(
                {"error": "Only patients can create logs."}
            ), 403
        # Guard clause; return error if logged in patient does not match patient_id
        # THIS IS BROKEN?! FIX IT AND ADD SCREENSHOT TO README under 'ins pat log post'
        if get_jwt_identity() != patient_id:
            return jsonify(
                {"error": "Logged in patient does not match patient_id."}
            ), 403

        # Fetch body of HTTP request
        body_data = request.get_json()

        # remember to validate input!
        # Define new instance of Log class
        log = Log(
            date=body_data.get("date") or date.today(),
            notes=body_data.get("notes"),

            # validate this!
            # change this to match create_app()... change route, incl in Insomnia
            patient_id=patient_id
        )

        # Add log to session and commit changes to database
        db.session.add(log)
        db.session.commit()

        # Return log object serialised according to the log schema
        return log_schema.dump(log), 201

    # In case the ?
    except IntegrityError as e:
        return jsonify(
            {"error": f"Patient ID {patient_id} not found."}
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


############################################

# http://localhost:5000/patients/<int:patient_id>/logs/
@logs_bp.route("/")
@jwt_required()
# Authorise patients and doctors to view logs they are involved with, with an early exit for admins
@authorise_as_log_viewer
def get_patient_logs(patient_id):
    """Get all logs for a particular patient.

    Args:
        patient_id (int): Patient primary key.

    Returns:
        JSON: All log details for the given patient.
    """

    try:

        # Create SQLAlchemy query statement:
        # SELECT logs.log_id, logs.date, logs.notes, logs.patient_id
        # FROM logs
        # WHERE logs.patient_id = :patient_id_1
        # ORDER BY logs.date;
        stmt = db.select(
            Log
        ).filter_by(
            patient_id=patient_id
        ).order_by(
            Log.date
        )

        # Execute statement, fetch all resulting values(?)
        logs = db.session.scalars(stmt).fetchall()

        # Guard clause; return error if no logs exist
        if not logs:
            return jsonify(
                {"error": f"Patient {patient_id} not found, or they have no logs."}
            ), 404

        # Return log objects serialised according to the logs schema
        return logs_schema.dump(logs)

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500

############################################

# http://localhost:5000/patients/<int:patient_id>/logs/<int:log_id>


@logs_bp.route("/<int:log_id>")
@jwt_required()
# Authorise patients and doctors to view logs they are involved with, with an early exit for admins
@authorise_as_log_viewer
def get_a_log(patient_id, log_id):
    """Get a particular log.

    Args:
        patient_id (int): Patient primary key.
        log_id (int): Log primary key.

    Returns:
        JSON: Serialised details of the patient log.
    """

    try:

        # Create SQLAlchemy query statement:
        # SELECT logs.log_id, logs.date, logs.notes, logs.patient_id
        # FROM logs
        # WHERE logs.patient_id = :patient_id_1
        # AND logs.log_id = :log_id_1;
        stmt = db.select(
            Log
        ).filter_by(
            patient_id=patient_id,
            log_id=log_id
        )

        # Connect to database session, execute statement, store resulting value
        log = db.session.scalar(stmt)

        # Guard clause; return error if log doesn't exist
        if not log:
            return jsonify(
                {"error": f"Patient {patient_id} or log {log_id} not found."}
            ), 404

        # Return log object serialised according to the log schema
        return log_schema.dump(log)

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


############################################

# http://localhost:5000/patients/<int:patient_id>/logs/<int:log_id>
@logs_bp.route("/<int:log_id>", methods=["PUT", "PATCH"])
@jwt_required()
# Authorise patients to update their own logs, with an early exit for admins
@authorise_as_log_owner
def update_log(patient_id, log_id):
    """Edit a log.

    Args:
        patient_id (int): Patient primary key.
        log_id (int): Log primary key.

    Returns:
        JSON: Serialised and updated log details.
    """
    try:
        # Fetch body of HTTP request
        body_data = request.get_json()

        # Create SQLAlchemy query statement:
        # SELECT logs.log_id, logs.date, logs.notes, logs.patient_id
        # FROM logs
        # WHERE logs.patient_id = :patient_id_1
        # AND logs.log_id = :log_id_1;
        stmt = db.select(
            Log
        ).filter_by(
            patient_id=patient_id,
            log_id=log_id
        )

        # Connect to database session, execute statement, store resulting value
        log = db.session.scalar(stmt)

        # Guard clause; return error if log doesn't exist
        if not log:
            return jsonify(
                {"error": f"Patient {patient_id} or log {log_id} not found."}
            ), 404

        # ?
        log.date = body_data.get("date") or log.date
        log.notes = body_data.get("notes") or log.notes
        # Do it for FK too? No. A log is not realistically going to change patients.

        # Commit changes to database
        db.session.commit()

        # Return updated log object serialised according to the log schema
        return log_schema.dump(log)

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


############################################

# http://localhost:5000/patients/<int:patient_id>/logs/<int:log_id>
@logs_bp.route("/<int:log_id>", methods=["DELETE"])
@jwt_required()
# Authorise patients to delete their own logs, with an early exit for admins
@authorise_as_log_owner
def delete_log(patient_id, log_id):
    """Delete a log.

    Args:
        log_id (int): Log primary key.

    Returns:
        JSON: Success message.
    """

    try:

        # Create SQLAlchemy query statement:
        # SELECT logs.log_id, logs.date, logs.notes, logs.patient_id
        # FROM logs
        # WHERE logs.patient_id = :patient_id_1
        # AND logs.log_id = :log_id_1;
        stmt = db.select(
            Log
        ).filter_by(
            patient_id=patient_id,
            log_id=log_id
        )

        # Connect to database session, execute statement, store resulting value
        log = db.session.scalar(stmt)

        # Guard clause; return error if log doesn't exist
        if not log:
            return jsonify(
                {"error": f"Patient {patient_id} or log {log_id} not found."}
            ), 404

        # Delete log and commit changes to database
        db.session.delete(log)
        db.session.commit()

        # Return serialised success message
        return jsonify(
            {"message": f"Log {log_id} deleted."}
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
