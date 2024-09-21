# TO DO:
# figure out privacy settings.

# somehow authorise doctors to view logs, but not all logs. you may not want your dentist viewing your psychology details.

# in case of emergency/hospital/ambulance etc, there should be some contingency access for health professionals like paramedics, surgeons, ER doctors/nurses, etc

###########################################################################

from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from init import db, bcrypt
from models import Patient, patient_schema, Doctor, doctor_schema

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

###########################################################################

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

###########################################################################

# http://localhost:5000/auth/register/<user_type>
@auth_bp.route("/register/<user_type>", methods=["POST"])
def register_user(user_type):
    try:
        # fetch data, deserialise it, store in variable
        body_data = request.get_json()

        if user_type not in ["patient", "doctor"]:
            return jsonify(
                {
                    "error": f"User type '{user_type}' not valid. URL must include '/auth/register/patient' or '/auth/register/doctor'."
                }
            ), 400

        # fields common to both patient and doctor
        email = body_data.get("email")
        password = body_data.get("password")
        name = body_data.get("name")
        sex = body_data.get("sex")
        is_admin = body_data.get("is_admin", False)

        if user_type == "patient":
            # remember to validate input!
            # define new instance of Patient class
            user = Patient(
                name=name,
                email=email,
                dob=body_data.get("dob"),
                sex=sex,
                is_admin=is_admin
            )

            schema = patient_schema

        elif user_type == "doctor":
            user = Doctor(
                name=name,
                email=email,
                sex=sex,
                specialty=body_data.get("specialty"),
                is_admin=is_admin
            )

            schema = doctor_schema

        # guard clause
        if not password:
            return jsonify({"error": "Password required."}), 400
        
        # hash password separately
        user.password = bcrypt.generate_password_hash(
            password).decode("utf-8")

        db.session.add(user)
        db.session.commit()

        return schema.dump(user), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # return jsonify({"error": "Email address is required"}), 400
            return jsonify(
                {
                    "error": f"The column {err.orig.diag.column_name} is required."
                }
            ), 400

        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return jsonify(
                {
                    "error": "Email address must be unique."
                }
            ), 400

###########################################################################

# doctor and patient emails must be unique within one type of model, but a doctor can duplicate themselves as a patient with the same email no worries. BUT! that will cause confusion with logging in. how do you know what someone is trying to log in as? use roles?

# http://localhost:5000/auth/login/<user_type>
@auth_bp.route("/login/<user_type>", methods=["POST"])
def login_user(user_type):
    # try:

    # fetch data, deserialise it, store in variable
    body_data = request.get_json()

    if user_type not in ["patient", "doctor"]:
        return jsonify({
            "error": f"User type '{user_type}' not valid. URL must include '/auth/login/patient' or '/auth/login/doctor'."
        }), 400

    email = body_data.get("email")
    password = body_data.get("password")

    # guard clause
    if not email or not password:
        return jsonify({"error": "Email and password required."}), 400

    if user_type == "patient":
        # create SQL statement
        # SELECT ...
        stmt = db.select(Patient).filter_by(email=email)
        user = db.session.scalar(stmt)
        user_id = user.patient_id
        schema = patient_schema

    elif user_type == "doctor":
        # create SQL statement
        # SELECT ...
        stmt = db.select(Doctor).filter_by(email=email)
        user = db.session.scalar(stmt)
        user_id = user.doctor_id
        schema = doctor_schema

    # guard clause
    if not user:
        return jsonify({"error": f"User account '{email}' not found. Please register user or initialise database."}), 404

    # is 'password' a keyword for this function? will this give me issues?:
    # guard clause
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid password."}), 401

    token = create_access_token(
        identity=str(user_id),
        additional_claims={
            "email": user.email,
            "user_type": user_type,
            "is_admin": user.is_admin
        },
        expires_delta=timedelta(days=1)
    )

    return jsonify({
        "email": email,
        "is_admin": user.is_admin,
        "user_type": user_type,
        "token": token
    })

    # except ... as ?:
