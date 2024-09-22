# TO DO:
# figure out privacy settings.

# somehow authorise doctors to view logs, but not all logs. you may not want your dentist viewing your psychology details.

# in case of emergency/hospital/ambulance etc, there should be some contingency access for health professionals like paramedics, surgeons, ER doctors/nurses, etc

###########################################################################

from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError

from init import db, bcrypt
from models import Patient, PatientSchema, patient_schema, Doctor, DoctorSchema, doctor_schema


from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

###########################################################################

# create auth blueprint with url prefix
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

###########################################################################

# http://localhost:5000/auth/register/<user_type>
@auth_bp.route("/register/<user_type>", methods=["POST"])
def register_user(user_type):
    """_summary_

    Args:
        user_type (_type_): _description_

    Returns:
        _type_: _description_
    """

    # Guard clause to escape function early if user type is invalid
    if user_type not in ["patient", "doctor"]:
        return jsonify(
            {
                "error": f"User type '{user_type}' not valid. URL must include '/auth/register/patient' or '/auth/register/doctor'."
            }
        ), 400
        
    try:
        # load data according to schema (this allows email regex to work), deserialise it, store in variable
        if user_type == "patient":
            body_data = PatientSchema().load(request.get_json())
            user = Patient(**body_data)
            schema = patient_schema
            
        elif user_type == "doctor":
            body_data = DoctorSchema().load(request.get_json())
            user = Doctor(**body_data)
            schema = doctor_schema

        # Guard clause
        password = body_data.get("password")  # use .pop() instead for security?
        if not password:
            return jsonify({"error": "Password required."}), 400

        # hash password separately
        user.password = bcrypt.generate_password_hash(
            password).decode("utf-8")

        db.session.add(user)
        db.session.commit()

        return schema.dump(user), 201

    # when would this one actually arise? do i need it? i've already handled invalid emails haven't I?
    # except ValidationError as e:
    #     return jsonify(e.messages), 400

    # if the date entered is invalid e.g. "2024-0101"
    except DataError as e:
        return jsonify({"error": "Invalid date formatting."}), 400

    # if the 
    except IntegrityError as e:
        if e.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # return jsonify({"error": "Email address is required"}), 400
            return jsonify(
                {
                    "error": f"The column {e.orig.diag.column_name} is required."
                }
            ), 400

        if e.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return jsonify(
                {
                    "error": "Email address must be unique."
                }
            ), 400

    # except Exception as e:
    #     return jsonify(
    #         {
    #             "error": "...?"
    #         }
    #     ), 400  # ?


###########################################################################

# doctor and patient emails must be unique within one type of model, but a doctor can duplicate themselves as a patient with the same email no worries. BUT! that will cause confusion with logging in. how do you know what someone is trying to log in as? use roles?

# http://localhost:5000/auth/login/<user_type>
@auth_bp.route("/login/<user_type>", methods=["POST"])
def login_user(user_type):
    """_summary_

    Args:
        user_type (_type_): _description_

    Returns:
        _type_: _description_
    """

    # try:

    # fetch data, deserialise it, store in variable
    body_data = request.get_json()

    if user_type not in ["patient", "doctor"]:
        return jsonify({
            "error": f"User type '{user_type}' not valid. URL must include '/auth/login/patient' or '/auth/login/doctor'."
        }), 400

    email = body_data.get("email")
    password = body_data.get("password")  # use .pop() instead for security?

    # Guard clause
    if not email or not password:
        return jsonify({"error": "Email and password required."}), 400

    if user_type == "patient":
        
        # Create SQLAlchemy query statement
        
        # SELECT ...
        
        stmt = db.select(Patient).filter_by(email=email)
        user = db.session.scalar(stmt)
        user_id = user.patient_id
        schema = patient_schema

    elif user_type == "doctor":
        
        # Create SQLAlchemy query statement
        
        # SELECT ...
        # ;
        
        stmt = db.select(Doctor).filter_by(email=email)
        user = db.session.scalar(stmt)
        user_id = user.doctor_id
        schema = doctor_schema

    # Guard clause
    if not user:
        return jsonify({"error": f"User account '{email}' not found. Please register user or initialise database."}), 404

    # is 'password' a keyword for this function? will this give me issues?:
    # Guard clause
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
