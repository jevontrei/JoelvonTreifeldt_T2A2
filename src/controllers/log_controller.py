from init import db
from models import Log, log_schema, logs_schema
from utils import authorise_as_patient_creator

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from datetime import date

############################################

logs_bp = Blueprint("logs", __name__, url_prefix="/logs")

############################################

@logs_bp.route("/")
@jwt_required()
# @authorise_as_participant
def get_all_logs():
    # SELECT * FROM logs ORDER BY ... ?;
    stmt = db.select(Log).order_by(Log.date)
    print(stmt)

    logs = db.session.scalars(stmt)
    return logs_schema.dump(logs)

############################################

@logs_bp.route("/<int:log_id>")
@jwt_required()
# @authorise_as_participant
def get_a_log(log_id):
    # SELECT * FROM logs WHERE log_id = log_id ... ?;
    stmt = db.select(Log).filter_by(log_id=log_id)
    print(stmt)

    log = db.session.scalar(stmt)
    return log_schema.dump(log)

############################################


  
# need an "if not ..." statement here somewhere (done for this one) (and in all other routes) to avoid returning an empty list for e.g. patient_id=9999 
    
    
# http://localhost:5000/logs/patients/<int:patient_id>
@logs_bp.route("/patients/<int:patient_id>")
@jwt_required()
# @authorise_as_participant
def get_patient_logs(patient_id):
    """
    Get all logs for a particular patient

    Args:
        patient_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # SELECT * FROM logs WHERE patient_id = patient_id ... ?;
    stmt = db.select(Log).filter_by(patient_id=patient_id)
    print(stmt)

    logs = db.session.scalars(stmt).fetchall()
    
    # guard clause
    if not logs:
        return jsonify({"message": f"No logs found for patient {patient_id}."}), 404
    
    return logs_schema.dump(logs)

############################################

# http://localhost:5000/logs/patients/<int:patient_id>
@logs_bp.route("/patients/<int:patient_id>/", methods=["POST"])
@jwt_required()
def create_log(patient_id):
    body_data = request.get_json()
    
    # remember to validate input!
    # define new instance of Log class
    log = Log(
        date=body_data.get("date") or date.today(),
        symptom=body_data.get("symptom"),
        duration=body_data.get("duration"),
        severity=body_data.get("severity"),
        
        # validate this!
        # change this to match create_app()... change route, incl in Insomnia
        patient_id=patient_id
    )

    db.session.add(log)
    db.session.commit()

    return log_schema.dump(log), 201

############################################

# http://localhost:5000/logs/<int:log_id>
@logs_bp.route("/<int:log_id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_patient_creator
def update_log(log_id):
    body_data = request.get_json()
    
    # create SQL statement
    # SELECT * FROM logs WHERE log_id = log_id ... ?;
    stmt = db.select(Log).filter_by(log_id=log_id)
    print(stmt)

    
    log = db.session.scalar(stmt)
    if log:
        log.date = body_data.get("date") or log.date
        log.symptom = body_data.get("symptom") or log.symptom
        log.duration = body_data.get("duration") or log.duration
        log.severity = body_data.get("severity") or log.severity
        # Do it for FK too? Probably not. A log is not realistically going to change patients
        db.session.commit()
        return log_schema.dump(log)
    else:
        return jsonify({"error": f"Log {log_id} not found."}), 404

############################################


# http://localhost:5000/logs/<int:log_id>
@logs_bp.route("/<int:log_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_patient_creator  # need to pass in log_id?
def delete_log(log_id):
    
    # SELECT * FROM logs WHERE log_id = log_id ... ?;
    stmt = db.select(Log).filter_by(log_id=log_id)
    print(stmt)

    log = db.session.scalar(stmt)
    
    if log:
        db.session.delete(log)
        db.session.commit()
        return jsonify({"message": f"Log {log_id} deleted."})  # , 200
    
    else:
        return jsonify({"error": f"Log {log_id} not found."}), 404

