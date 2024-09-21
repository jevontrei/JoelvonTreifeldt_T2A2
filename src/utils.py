from models import Patient, Doctor
from init import db

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
import functools

##############################################################

# ADAPT ALL THIS (FROM TRELLO APP)

# decorator function for admins


def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        print(f"user_id: {user_id}")

        if ...:
            stmt = db.select(Patient).filter_by(user_id=user_id)

        elif ...:
            stmt = db.select(Doctor).filter_by(user_id=user_id)

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
