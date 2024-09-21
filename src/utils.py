from models import Patient
from init import db

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
import functools

##############################################################

## ADAPT ALL THIS (FROM TRELLO APP)

# decorator function for authorising as admin 
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        print(f"user_id: {user_id}")
    
        stmt = db.select(User).filter_by(id=user_id)
        
        user = db.session.scalar(stmt)
        
        if user.is_admin:
            return fn(*args, **kwargs)
        
        else:
            return jsonify({"error", "Only admins can perform this action."}), 403
        
    return wrapper

##############################################################

# and do for doctors as well?!

##############################################################

# for patients to update/delete their logs
# def authorise_as_creator(fn):
#     @functools.wraps(fn)
#     def wrapper(*args, **kwargs):
#         user_id = get_jwt_identity()
        
# ##############################################################

# for patients OR doctors as specified in Treatments tables
# def authorise_participant(fn):
#     @functools.wraps(fn)
#     def wrapper(*args, **kwargs):
#         user_id = get_jwt_identity()
