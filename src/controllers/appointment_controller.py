from init import db
from models.models import Appointment, appointment_schema, appointments_schema
from main import app


##################################################

@app.route("/appointments/")
def get_all_appointments():
    stmt = db.select(Appointment).order_by(Appointment.datetime)
    appointments = db.select.scalars(stmt)
    return appointments_schema.dump(appointments)

##################################################

@app.route("/appointments/<int:appt_id>")
def get_appointments(appt_id):
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)
    appointment = db.session.scalar(stmt)
    return appointment_schema.dump(appointment)

##################################################

# GOAL: get all appointments for a particular patient

# this is complicated becuase it's not patient_id, it's auth_id. how to query auth using patient_id?

@app.route("/appointments/patients/<int:patient_id>")
def get_someones_appointments(patient_id):
    stmt = db.select(Appointment).filter_by(patient_id=patient_id)
    appointments = db.session.scalars(stmt)
    return appointments_schema.dump(appointments)

