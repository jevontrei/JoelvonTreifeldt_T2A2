from models import Patient, Doctor, Log, Treatment  # , log_schema
from init import db

import functools
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt, get_jwt_header
# from sqlalchemy.exc import NoResultFound

##############################################################

# how to implement this without preventing non-admins from accessing the function?


def authorise_as_admin(fn):
    """Decorator that authorises administrators to perform sensitive/important tasks.

    Args:
        fn (function): _description_

    Returns:
        _type_: _description_
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        jwt = get_jwt()

        # Guard clause; return error if user is not an admin
        if not jwt.get("is_admin"):
            return jsonify(
                {"error": "Only admins can perform this action."}
            ), 403

        return fn(*args, **kwargs)

    return wrapper

##############################################################


def authorise_as_log_viewer(fn):
    """Decorator that authorises patients and doctors to view logs.

    Args:
        fn (function): _description_

    Returns:
        _type_: _description_
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        # Fetch patient_id, current user type and ID
        jwt = get_jwt()
        patient_id = kwargs.get("patient_id")
        user_type = jwt.get("user_type")
        logged_in_id = get_jwt_identity()

        # Check if user is a patient or doctor
        if user_type == "patient":
            # patient_id must match the log's patient_id
            if str(patient_id) != logged_in_id:
                return jsonify(
                    {"error": "Only the log creator patient has manage access."}
                ), 403

            # Allow function to execute
            return fn(*args, **kwargs)

        elif user_type == "doctor":
            # doctor_id must be associated with the log's patient_id through the Treatments table

            # Create SQLAlchemy query statement:
            # SELECT *
            # FROM treatments
            # WHERE patient_id = :patient_id_1
            # AND doctor_id = :doctor_id_1;
            stmt = db.select(
                Treatment
            ).filter_by(
                patient_id=patient_id, doctor_id=logged_in_id
            )

            # Execute statement, fetch all resulting values
            # change this? only need one positive result
            treatment = db.session.scalars(stmt).fetchall()

            # Guard clause; return error if no such doctor-patient relationship exists
            if not treatment:
                return jsonify(
                    {"error": "Only authorised doctors can access this log."}
                ), 403

            # Allow function to execute
            return fn(*args, **kwargs)

    # Return wrapper function
    return wrapper

# ##############################################################


def authorise_as_log_owner(fn):
    """Decorator that authorises the owner of the log to update and delete it.

    Args:
        fn (function): _description_
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Fetch patient_id, current user type and ID
        jwt = get_jwt()
        patient_id = kwargs.get("patient_id")
        logged_in_id = get_jwt_identity()

        # Guard clause; return error if patient_id does not match logged_in_id
        if str(patient_id) != logged_in_id:
            return jsonify({"error": "Only the log owner has manage access."}), 403

        # Allow function to execute
        return fn(*args, **kwargs)

    # Return wrapper function
    return wrapper

# ##############################################################


def authorise_treatment_participant(fn):
    """Decorator that authorises patients OR doctors (as specified in Treatments tables) to view logs and manage appointments

    Args:
        fn (function): _description_
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Fetch user_id, user_type
        user_id = get_jwt_identity()
        user_type = get_jwt().get("user_type")

        # Fetch treatment_id from kwargs
        treatment_id = kwargs.get("treatment_id")

        # Create SQLAlchemy query statement:
        # SELECT *
        # FROM treatments
        # WHERE treatment_id = :treatment_id_1;
        stmt = db.select(Treatment).filter_by(treatment_id=treatment_id)

        # Execute statement, fetch all resulting values
        treatment = db.session.scalars(stmt).first()

        # Guard clause; return error if no such doctor-patient relationship exists

        # Guard clause; return error if no such treatment exists
        if not treatment:
            return jsonify(
                {"error": "Treatment not found."}
            ), 404

        # Fetch patient_id and doctor_id from treatment
        patient_id = treatment.patient_id
        doctor_id = treatment.doctor_id

        # Check user type
        if user_type == "patient":
            # patient_id must match the user_id
            if str(patient_id) != user_id:
                return jsonify(
                    {"error": "Only authorised patients can access this resource."}
                ), 403

        elif user_type == "doctor":
            # doctor_id must match the user_id
            if str(doctor_id) != user_id:
                return jsonify(
                    {"error": "Only authorised doctors can access this resource."}
                ), 403

        # Allow function to execute
        return fn(*args, **kwargs)

    # Return wrapper function
    return wrapper
