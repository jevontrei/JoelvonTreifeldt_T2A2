from init import db
from main import app
from models.models import Log, log_schema, logs_schema

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

