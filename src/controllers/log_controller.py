from init import db
from main import app
from models.models import Log, log_schema, logs_schema
from flask import request
from datetime import date


############################################


@app.route("/logs/")
def get_all_logs():
    # SELECT * FROM logs ORDER BY ... ?;
    stmt = db.select(Log).order_by(Log.date)
    logs = db.session.scalars(stmt)
    return logs_schema.dump(logs)

############################################


@app.route("/logs/<int:log_id>")
def get_a_log(log_id):
    # SELECT * FROM logs WHERE log_id = log_id ... ?;
    stmt = db.select(Log).filter_by(log_id=log_id)
    log = db.session.scalar(stmt)
    return log_schema.dump(log)

############################################

# change route to /patients/<int:patient_id>/logs/?


@app.route("/logs/patients/<int:patient_id>")
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
    
    
    # need an if statement here somewhere (and in all other routes) to avoid returning an empty list for e.g. patient_id=9999 
    
    
    logs = db.session.scalars(stmt)
    
    return logs_schema.dump(logs)


############################################


@app.route("/patients/<int:patient_id>/logs/", methods=["POST"])
def create_log(patient_id):
    body_data = request.get_json()
    # SELECT * FROM logs WHERE log_id = log_id... ?;
    stmt = db.select(Log)  # .filter_by(log_id=log_id)
    log = db.session.scalar(stmt)

    if log:
        log = Log(
            date=body_data.get("date") or date.today(),
            symptom=body_data.get("symptom"),
            duration=body_data.get("duration"),
            severity=body_data.get("severity"),
            patient_id=patient_id
        )

        db.session.add(log)
        db.session.commit()

        return log_schema.dump(log), 201

    else:
        return {"error": f"Log {log_id} not found."}

############################################

# change route to /patients/<int:patient_id>/logs/?


@app.route("/logs/<int:log_id>", methods=["PUT", "PATCH"])
def update_log(log_id):
    body_data = request.get_json()
    
    # create SQL statement
    # SELECT * FROM logs WHERE log_id = log_id ... ?;
    stmt = db.select(Log).filter_by(log_id=log_id)
    
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
        return {"error": f"Log {log_id} not found."}, 404

############################################

# change route to /patients/<int:patient_id>/logs/?


@app.route("/logs/<int:log_id>", methods=["DELETE"])
def delete_log(log_id):
    # check for authorisation
    # SELECT * FROM logs WHERE log_id = log_id ... ?;
    stmt = db.select(Log).filter_by(log_id=log_id)
    log = db.session.scalar(stmt)
    if log:
        db.session.delete(log)
        db.session.commit()
        return {"message": f"Log {log_id} deleted."}  # , 200
    else:
        return {"error": f"Sorry, log {log_id} not found."}  # , 404?

############################################
