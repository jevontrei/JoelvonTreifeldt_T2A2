from models import Patient, Doctor, Log, Treatment#, log_schema
from init import db

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt, get_jwt_header
import functools
# from sqlalchemy.exc import NoResultFound

##############################################################

# ADAPT ALL THIS (FROM TRELLO APP)

# decorator function for admins

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        jwt = get_jwt()
        
        # guard clause
        if not jwt.get("is_admin"):
            return jsonify({"error": "Only admins can perform this action."}), 403
        
        return fn(*args, **kwargs)

    return wrapper

##############################################################

# this is broken?!

# decorator function for patients to update/delete their logs
def authorise_as_patient_creator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print()
        
        patient_id = get_jwt_identity()
        log_id = kwargs.get('log_id')
        print(f"log_id: {log_id}")
        
        jwt = get_jwt()

        if jwt.get("user_type") != "patient":
            return jsonify({"error": "Only patients can manage logs."}), 403
        
        
        # create SQL statement
        # SELECT ...
        stmt = db.select(Log).filter_by(patient_id=patient_id)
        print(f"utils stmt: {stmt}")
        
        log = db.session.scalars(stmt).fetchall()
        print(f"log: {log}")

        # guard clause
        if not log:
            return jsonify({"error": f"No logs found."}), 404  # removed {log_id}
        
        if patient_id != str(log.patient_id):
            return jsonify({"error": "Only the log creator patient has manage access."}), 403
        
        return fn(*args, **kwargs)
    
    return wrapper


# ##############################################################

# FINISH THIS?!

# decorator function for authorised patients OR doctors (as specified in Treatments tables) to view logs and manage appointments
# def authorise_as_participant(fn):
#     @functools.wraps(fn)
#     def wrapper(*args, **kwargs):
#         user_id = get_jwt_identity()
