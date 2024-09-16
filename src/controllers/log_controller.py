from init import db
from main import app
from models.models import Log, log_schema, logs_schema
from flask import request
from datetime import date


############################################


@app.route("/logs/")
def get_all_logs():
    stmt = db.select(Log).order_by(Log.date)
    logs = db.session.scalars(stmt)
    return logs_schema.dump(logs)

############################################


@app.route("/logs/<int:log_id>")
def get_a_log(log_id):
    stmt = db.select(Log).filter_by(log_id=log_id)
    log = db.session.scalar(stmt)
    return log_schema.dump(log)

############################################


@app.route("/logs/patients/<int:patient_id>")
def get_patient_log(patient_id):
    stmt = db.select(Log).filter_by(patient_id=patient_id)
    print(stmt)
    logs = db.session.scalars(stmt)
    return logs_schema.dump(logs)


############################################

@app.route("/logs/<int:log_id>", methods=["DELETE"])
def delete_log(log_id):
    # check for authorisation
    stmt = db.select(Log).filter_by(log_id=log_id)
    log = db.session.scalar(stmt)
    if log:
        db.session.delete(log)
        db.session.commit()
        return {"message": f"Log {log_id} deleted."}  # , 200
    else:
        return {"error": f"Sorry, log {log_id} can't be found."}  # , 404?

############################################

# @app.route("/logs/", methods=["POST"])
@app.route("/patients/<int:patient_id>/logs/", methods=["POST"])
def create_log(patient_id):
    body_data = request.get_json()
    stmt = db.select(Log)  # .filter_by(log_id=log_id)
    log = db.session.scalar(stmt)
    
    if log:
        log = Log(
            date = body_data.get("date") or date.today(),
            symptom = body_data.get("symptom"),
            duration = body_data.get("duration"),
            severity = body_data.get("severity"),
            patient_id = patient_id
        )

        db.session.add(log)
        db.session.commit()

        return log_schema.dump(log), 201

    else:
        return {"error": f"Log {log_id} not found."}
    
############################################

# not sure if update route should be /logs/ or /logs/log_id
@app.route("/logs/<int:log_id>", methods=["PUT", "PATCH"])
def update_log(log_id): 
    body_data = request.get_json()
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
