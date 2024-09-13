from init import db
# from models.doctor import Doctor, doctor_schema, doctors_schema
from models.models import Doctor, doctor_schema, doctors_schema
from main import app


@app.route("/doctors/")
def get_all_doctors():
    stmt = db.select(Doctor).order_by(Doctor.name)
    doctors = db.session.scalars(stmt)
    return doctors_schema.dump(doctors)
