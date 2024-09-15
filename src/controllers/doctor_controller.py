from init import db
# from models.doctor import Doctor, doctor_schema, doctors_schema
from models.models import Doctor, doctor_schema, doctors_schema
from main import app

##################################################

@app.route("/doctors/")
def get_all_doctors():
    stmt = db.select(Doctor).order_by(Doctor.name)
    doctors = db.session.scalars(stmt)
    return doctors_schema.dump(doctors)

##################################################

@app.route("/doctors/<int:doc_id>")
def get_doctor(doc_id):
    stmt = db.select(Doctor).filter_by(doc_id=doc_id)
    doctor = db.session.scalar(stmt)
    return doctor_schema.dump(doctor)

##################################################
