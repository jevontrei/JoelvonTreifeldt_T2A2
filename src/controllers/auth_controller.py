# TO DO:
# - Figure out privacy settings.
# - Somehow authorise doctors to view logs, but not all logs. you may not want your dentist viewing your psychology details.
# - In case of emergency/hospital/ambulance etc, there should be some contingency access for health professionals like paramedics, surgeons, ER doctors/nurses, etc

###########################################################################

from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
# from marshmallow.exceptions import ValidationError

from init import db, bcrypt
from models import Patient, PatientSchema, patient_schema, Doctor, DoctorSchema, doctor_schema

from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

###########################################################################

# Create auth blueprint with URL prefix
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)

###########################################################################

# http://localhost:5000/auth/register/<user_type>


@auth_bp.route("/register/<user_type>", methods=["POST"])
def register_user(user_type):
    """Create a new patient or doctor user.

    Args:
        user_type (str): Patient or doctor primary key.

    Returns:
        Tuple: All registration details, serialised according to patient or doctor schema (JSON); a 201 HTTP response status code.
    """

    # Guard clause; escape function early if user type is invalid
    if user_type not in ["patient", "doctor"]:
        return jsonify(
            {"error": f"User type '{user_type}' not valid. URL must include '/auth/register/patient' or '/auth/register/doctor'."}
        ), 400

    try:
        # Load data according to schema, deserialise it, store in variable; create user instance with kwargs; assign correct schema
        if user_type == "patient":
            body_data = PatientSchema().load(request.get_json())
            user = Patient(**body_data)
            schema = patient_schema

        elif user_type == "doctor":
            body_data = DoctorSchema().load(request.get_json())
            user = Doctor(**body_data)
            schema = doctor_schema

        # Guard clause; return error if no password provided
        # .pop() increases secruity by removing password
        password = body_data.pop("password")
        if not password:
            return jsonify(
                {"error": "Password required."}
            ), 400

        # Hash password
        user.password = bcrypt.generate_password_hash(
            password).decode("utf-8")

        # Add user to session and commit changes to database
        db.session.add(user)
        db.session.commit()

        # Return user object serialised according to the corresponding schema
        return schema.dump(user), 201

    # In case the date entered has invalid format, e.g. "2024-0101"
    except DataError as e:
        return jsonify(
            {"error": "Invalid date formatting."}
        ), 400

    # If the email address (or other attribute) is missing or already taken
    except IntegrityError as e:
        if e.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return jsonify(
                {"error": f"The column {e.orig.diag.column_name} is required."}
            ), 400

        if e.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return jsonify(
                {"error": "Email address must be unique."}
            ), 400

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


###########################################################################

# http://localhost:5000/auth/login/<user_type>


@auth_bp.route("/login/<user_type>", methods=["POST"])
def login_user(user_type):
    """Create new logged-in session for a patient or doctor user.

    Args:
        user_type (str): Patient or doctor primary key.

    Returns:
        JSON: All login details, serialised according to the corresponding schema.
    """

    # Fetch body of HTTP request
    body_data = request.get_json()

    # Guard clause; return error if user type is invalid
    if user_type not in ["patient", "doctor"]:
        return jsonify(
            {"error": f"User type '{user_type}' not valid. URL must include '/auth/login/patient' or '/auth/login/doctor'."}
        ), 400

    email = body_data.get("email")
    # .pop() increases secruity by removing password
    password = body_data.pop("password")

    # Guard clause; return error if email or password missing
    if not email or not password:
        return jsonify(
            {"error": "Email and password required."}
        ), 400

    try:
        if user_type == "patient":
            # Create SQLAlchemy query statement:
            # SELECT *
            # FROM patients
            # WHERE patients.email = :email_1;
            stmt = db.select(
                Patient
            ).filter_by(
                email=email
            )

            # Connect to database session, execute statement, store resulting value
            user = db.session.scalar(stmt)
            user_id = user.patient_id
            # schema = patient_schema

        elif user_type == "doctor":
            # Create SQLAlchemy query statement:
            # SELECT *
            # FROM doctors
            # WHERE doctors.email = :email_1;
            stmt = db.select(
                Doctor
            ).filter_by(
                email=email
            )

            # Connect to database session, execute statement, store resulting value
            user = db.session.scalar(stmt)
            user_id = user.doctor_id
            # schema = doctor_schema

    # Return error if user doesn't exist
    except AttributeError as e:
        return jsonify(
            {"error": "Email address not found. Please register user or initialise database."}
        ), 404

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500

    # Guard clause; return error if password doesn't match stored hash
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify(
            {"error": "Invalid password."}
        ), 401

    # Create JWT with additional details for use elsewhere
    token = create_access_token(
        identity=str(user_id),
        additional_claims={
            "email": user.email,
            "user_type": user_type,
            "is_admin": user.is_admin
        },
        expires_delta=timedelta(days=1)
    )

    # Return serialised login details
    return jsonify(
        {
            "email": email,
            "is_admin": user.is_admin,
            "user_type": user_type,
            "token": token
        }
    )
