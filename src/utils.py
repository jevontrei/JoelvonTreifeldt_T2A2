from models import Patient, Doctor, Log, Treatment#, log_schema
from init import db

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt, get_jwt_header
import functools
# from sqlalchemy.exc import NoResultFound

##############################################################

def authorise_as_admin(fn):
    """Decorator that authorises administrators to perform sensitive/important tasks. Admins can ..., ? is there anything they can't do?

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
            return jsonify({"error": "Only admins can perform this action."}), 403
        
        return fn(*args, **kwargs)

    return wrapper

##############################################################

# this is broken?!

def authorise_as_patient_creator(fn):
    """Decorator that authorises patients (and no one else? not even admins?) to update and delete their own logs. N

    Args:
        fn (function): _description_

    Returns:
        _type_: _description_
    """
    
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print()
        
        patient_id = get_jwt_identity()
        log_id = kwargs.get('log_id')
        print(f"log_id: {log_id}")
        
        jwt = get_jwt()

        # Guard clause; return error if user is not a patient
        if jwt.get("user_type") != "patient":
            return jsonify({"error": "Only patients can manage logs."}), 403
        
        # Create SQLAlchemy query statement:
        
        # SELECT ...
        # ;
        
        stmt = db.select(Log).filter_by(patient_id=patient_id)
        
        log = db.session.scalars(stmt).fetchall()

        # Guard clause; return error if log doesn't exist
        if not log:
            return jsonify({"error": f"No logs found."}), 404  # removed {log_id}
        
        # Guard clause; return error if user is not the patient who created this log
        if patient_id != str(log.patient_id):
            return jsonify({"error": "Only the log creator patient has manage access."}), 403
        
        # Allow function to execute
        return fn(*args, **kwargs)
    
    return wrapper

# ##############################################################

# FINISH THIS?!

def authorise_as_participant(fn):
    """Decorator that authorises patients OR doctors (as specified in Treatments tables) to view logs and manage appointments

    Args:
        fn (function): _description_
    """
    
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
