from init import db, ma

from datetime import date


class Log(db.Model):
    __tablename__ = "logs"
    
    # make sure i allow duplicate dates... so a patient can make multiple logs in one day

    log_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, nullable=False)  # is it redundant to use nullable=False AND a default date?
    
    # CHANGE NAME TO NOTES... include word limit?!
    symptom = db.Column(db.String(100), nullable=False)
    
    # str, not int, to facilitate multiple timescales
    # changed symptom to notes, so delete duration and severity
    duration = db.Column(db.String)
    
    # changed symptom to notes, so delete duration and severity
    severity = db.Column(db.String)

    # FK from patient (many-to-one)
    patient_id = db.Column(db.Integer, db.ForeignKey(
        "patients.patient_id", ondelete="CASCADE"), nullable=False)

    # many-to-one?
    patient = db.relationship("Patient", back_populates="logs")


class LogSchema(ma.Schema):
    class Meta:
        fields = ("log_id", "date", "symptom",
                  "duration", "severity", "patient_id")


log_schema = LogSchema()
logs_schema = LogSchema(many=True)
