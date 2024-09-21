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
        jwt = get_jwt()
        
        if not jwt.get("is_admin"):
            return jsonify({"error": "Only admins can perform this action."}), 403
        
        return fn(*args, **kwargs)

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
