from init import db
from main import app
from models.models import Log, log_schema, logs_schema

@app.route("/logs/")
def get_all_logs():
    stmt = db.select(Log)
    logs = db.session.scalars(stmt)
    return logs_schema.dump(logs)

############################################

@app.route("/logs/<int:log_id>")
def get_a_logs():
    stmt = db.select(Log)
    log = db.session.scalar(stmt)
    return log_schema.dump(log)