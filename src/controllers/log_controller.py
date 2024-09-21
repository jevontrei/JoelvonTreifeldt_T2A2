from init import db
from models import Log, log_schema, logs_schema
from utils import authorise_as_patient_creator

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from datetime import date

############################################

logs_bp = Blueprint("logs", __name__, url_prefix="/logs")

# change all routes to start with /patients/<int:patient_id>/logs/ ? prob makes more sense

############################################

# DELETE THIS ROUTE - not practical for the real world // security risk?

# # http://localhost:5000/logs/
# @logs_bp.route("/")
# @jwt_required()
# # @authorise_as_participant
# def get_all_logs():
#     # SELECT * FROM logs ORDER BY ... ?;
#     stmt = db.select(Log).order_by(Log.date)
#     print(stmt)

#     logs = db.session.scalars(stmt)
#     return logs_schema.dump(logs)

############################################

# change this to be specific to a patient_id as well as a log_id?
# http://localhost:5000/logs/<int:log_id>
@logs_bp.route("/<int:log_id>")
@jwt_required()
# justify this decorator auth choice
# @authorise_as_participant
def get_a_log(log_id):
    # SELECT * FROM logs WHERE log_id = log_id ... ?;
    stmt = db.select(Log).filter_by(log_id=log_id)
    print(stmt)

    log = db.session.scalar(stmt)
    
    if not log:
        return jsonify({"message": f"Log {log_id} not found."}), 404
    
    return log_schema.dump(log)

############################################

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
    stmt = db.select(Log).filter_by(patient_id=patient_id)#.order_by()
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
        notes=body_data.get("notes"),
        
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
        log.notes = body_data.get("notes") or log.notes
        # Do it for FK too? No. A log is not realistically going to change patients.
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

