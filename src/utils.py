from models import Patient, Doctor
from init import db

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt, get_jwt_header
import functools
from sqlalchemy.exc import NoResultFound

##############################################################

# ADAPT ALL THIS (FROM TRELLO APP)

# decorator function for admins

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # use JWT to fetch the user ID (patient_id or doctor_id) and store it in a variable
        
        print()
        
        user_id = get_jwt_header()
        print(f"user_id: {user_id}; type: {type(user_id)}")
        
        print()

        user_id = get_jwt()
        print(f"user_id: {user_id}; type: {type(user_id)}")

        print()

        user_id = get_jwt_identity()
        print(f"user_id: {user_id}; type: {type(user_id)}")

        # HOW DO I CHECK IF THE USER IS A PATIENT OR A DOCTOR?
        # if ...:
        try:
            stmt = db.select(Patient).filter_by(patient_id=user_id)
            print(f"patient stmt: {stmt}")
            user = db.session.scalar(stmt)

        except NoResultFound:
            ...
        # user = db.session.scalar(stmt)

        # elif ...:
        stmt = db.select(Doctor).filter_by(doctor_id=user_id)
        print(f"doctor stmt: {stmt}")
        
        # stmt = db.select(Patient).filter_by(patient_id=user_id) or db.select(Doctor).filter_by(doctor_id=user_id)

        user = db.session.scalar(stmt)

        if user.is_admin:
            return fn(*args, **kwargs)

        else:
            return jsonify({"error": "Only admins can perform this action."}), 403

    return wrapper

##############################################################

# decorator function for patients to update/delete their logs
# def authorise_as_creator(fn):
#     @functools.wraps(fn)
#     def wrapper(*args, **kwargs):
#         user_id = get_jwt_identity()

# ##############################################################

# decorator function for authorised patients OR doctors (as specified in Treatments tables) to manage logs and appointments
# def authorise_as_participant(fn):
#     @functools.wraps(fn)
#     def wrapper(*args, **kwargs):
#         user_id = get_jwt_identity()
