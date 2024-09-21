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
                    "message": f"User type '{user_type}' not valid. URL must include '/auth/register/patient' or '/auth/register/doctor'."
                }
            ), 400

        if user_type == "patient":

            # remember to validate input!
            # define new instance of Patient class
            patient = Patient(
                name=body_data.get("name"),
                email=body_data.get("email"),
                # password=body_data.get("password"),
                dob=body_data.get("dob"),
                sex=body_data.get("sex"),
                is_admin=body_data.get("is_admin")
            )

            # hash password separately
            password = body_data.get("password")
            if password:
                patient.password = bcrypt.generate_password_hash(
                    password).decode("utf-8")

            db.session.add(patient)
            db.session.commit()

            return patient_schema.dump(patient), 201

        elif user_type == "doctor":

            doctor = Doctor(
                name=body_data.get("name"),
                email=body_data.get("email"),
                # password=body_data.get("password")#,
                sex=body_data.get("sex"),
                is_admin=body_data.get("is_admin")
            )

            # hash password separately
            password = body_data.get("password")
            if password:
                doctor.password = bcrypt.generate_password_hash(
                    password).decode("utf-8")

            db.session.add(doctor)
            db.session.commit()

            return doctor_schema.dump(doctor), 201

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

        return jsonify(
            {
                "message": f"User type '{user_type}' not valid. URL must include '/auth/login/patient' or '/auth/login/doctor'."
            }
        ), 400

    if user_type == "patient":

        stmt = db.select(Patient).filter_by(email=body_data["email"])

        patient = db.session.scalar(stmt)

        if not patient:
            return jsonify({"message": f"Patient account '{body_data['email']}' not found. Please register user or initialise database."}), 404

        if patient and bcrypt.check_password_hash(patient.password, body_data.get("password")):

            token = create_access_token(
                identity=str(patient.patient_id),
                expires_delta=timedelta(days=1)
            )

            return jsonify(
                {
                    "email": patient.email,
                    "is_admin": patient.is_admin,
                    "token": token
                }
            )

    elif user_type == "doctor":

        stmt = db.select(Doctor).filter_by(email=body_data["email"])

        doctor = db.session.scalar(stmt)

        if not doctor:
            return jsonify({"message": f"Doctor account '{body_data['email']}' not found. Please register user or initialise database."}), 404

        if doctor and bcrypt.check_password_hash(doctor.password, body_data.get("password")):

            token = create_access_token(
                identity=str(doctor.doctor_id),
                expires_delta=timedelta(days=1)
            )

            return jsonify(
                {
                    "email": doctor.email,
                    "is_admin": doctor.is_admin,
                    "token": token
                }
            )

    # what do i do with this?:
    else:
        return jsonify({"error": "Invalid email or password."}), 400

    # except ... as ?:

