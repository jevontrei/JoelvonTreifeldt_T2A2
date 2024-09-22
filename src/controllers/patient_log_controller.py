from sqlalchemy.exc import IntegrityError
from init import db
from models import Log, log_schema, logs_schema
from utils import authorise_as_patient_creator#, authorise_as_participant

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from datetime import date

############################################

# Create blueprint with URL prefix
# all logs (child) are located under the patient (parent) resource
logs_bp = Blueprint("logs", __name__, url_prefix="/patients/<int:patient_id>/logs")

############################################

# http://localhost:5000/patients/<int:patient_id>/logs/
@logs_bp.route("/", methods=["POST"])
@jwt_required()
def create_log(patient_id):
    """Create a new patient log.

    Args:
        patient_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        body_data = request.get_json()
        
        # remember to validate input!
        # define new instance of Log class
        log = Log(
            date=body_data.get("date") or date.today(),
            notes=body_data.get("notes"),
            
            # validate this!
            # change this to match create_app()... change route, incl in Insomnia
            patient_id=patient_id
        )

        db.session.add(log)
        db.session.commit()

        return log_schema.dump(log), 201
    
    except IntegrityError as e:
        return jsonify({"error": f"Patient id {patient_id} not found."}), 404

############################################

# http://localhost:5000/patients/<int:patient_id>/logs/
@logs_bp.route("/")
@jwt_required()
# justify deco choice
# @authorise_as_patient_creator
# @authorise_as_participant
def get_patient_logs(patient_id):
    """Get all logs for a particular patient.

    Args:
        patient_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    # Create SQLAlchemy query statement

    # stmt: SELECT logs.log_id, logs.date, logs.notes, logs.patient_id 
    # FROM logs 
    # WHERE logs.patient_id = :patient_id_1;

    stmt = db.select(Log).filter_by(patient_id=patient_id)#.order_by()

    # defs need fetchall() here?
    logs = db.session.scalars(stmt).fetchall()
    
    # Guard clause
    if not logs:
        return jsonify({"error": f"Patient {patient_id} not found, or they have no logs."}), 404
    
    return logs_schema.dump(logs)

############################################

# http://localhost:5000/patients/<int:patient_id>/logs/<int:log_id>
@logs_bp.route("/<int:log_id>")
@jwt_required()
# justify this decorator auth choice
# @authorise_as_participant
def get_a_log(patient_id, log_id):
    """Get a particular log.

    Args:
        patient_id (_type_): _description_
        log_id (_type_): _description_

    Returns:
        _type_: _description_
    """

    # Create SQLAlchemy query statement

    # SELECT logs.log_id, logs.date, logs.notes, logs.patient_id 
    # FROM logs 
    # WHERE logs.patient_id = :patient_id_1 
    # AND logs.log_id = :log_id_1;

    stmt = db.select(Log).filter_by(patient_id=patient_id, log_id=log_id)

    log = db.session.scalar(stmt)
    
    # Guard clause
    if not log:
        return jsonify({"error": f"Patient {patient_id} or log {log_id} not found."}), 404
    
    return log_schema.dump(log)

############################################

# http://localhost:5000/patients/<int:patient_id>/logs/<int:log_id>
@logs_bp.route("/<int:log_id>", methods=["PUT", "PATCH"])
@jwt_required()
# @authorise_as_patient_creator
def update_log(patient_id, log_id):
    """Edit a log.

    Args:
        patient_id (_type_): _description_
        log_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # fetch content of request
    body_data = request.get_json()
    
    # Create SQLAlchemy query statement
    
    # SELECT logs.log_id, logs.date, logs.notes, logs.patient_id 
    # FROM logs 
    # WHERE logs.patient_id = :patient_id_1 
    # AND logs.log_id = :log_id_1;
    
    stmt = db.select(Log).filter_by(patient_id=patient_id, log_id=log_id)
    
    log = db.session.scalar(stmt)
    
    # Guard clause
    if not log:
        return jsonify({"error": f"Patient {patient_id} or log {log_id} not found."}), 404
        
    log.date = body_data.get("date") or log.date
    log.notes = body_data.get("notes") or log.notes
    # Do it for FK too? No. A log is not realistically going to change patients.
    db.session.commit()
    return log_schema.dump(log)
    
############################################

# http://localhost:5000/patients/<int:patient_id>/logs/<int:log_id>
@logs_bp.route("/<int:log_id>", methods=["DELETE"])
@jwt_required()
# FIX THIS DECO?!:
# @authorise_as_patient_creator  # need to pass in log_id?
def delete_log(patient_id, log_id):
    """Delete a log.

    Args:
        log_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    # Create SQLAlchemy query statement

    # SELECT logs.log_id, logs.date, logs.notes, logs.patient_id 
    # FROM logs 
    # WHERE logs.patient_id = :patient_id_1 
    # AND logs.log_id = :log_id_1;

    stmt = db.select(Log).filter_by(patient_id=patient_id, log_id=log_id)

    log = db.session.scalar(stmt)

    # Guard clause
    if not log:
        return jsonify({"error": f"Patient {patient_id} or log {log_id} not found."}), 404

    db.session.delete(log)
    
    db.session.commit()
    
    return jsonify({"message": f"Log {log_id} deleted."})
    