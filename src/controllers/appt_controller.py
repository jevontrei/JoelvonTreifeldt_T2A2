from init import db
from models.models import Appointment, appointment_schema, appointments_schema, treat
from main import app


##################################################

@app.route("/appointments/")
def get_all_appointments():
    stmt = db.select(Appointment)  # .order_by(Appointment.datetime)
    print(f"stmt = {stmt}")
    appointments = db.session.scalars(stmt)
    return appointments_schema.dump(appointments)

##################################################


@app.route("/appointments/<int:appt_id>")
def get_appointment(appt_id):
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)
    print(stmt, type(stmt))
    appointment = db.session.scalar(stmt)
    return appointment_schema.dump(appointment)

##################################################

# GOAL: get all appointments for a particular patient

# this is complicated maybe? becuase it's not patient_id, it's treat_id. how to query treat using patient_id?

# this was working but not anymore since i renamed auth to treat?:

@app.route("/appointments/patients/<int:patient_id>")
def get_patient_appointments(patient_id):
    stmt = db.session.query(Appointment).join(treat).filter(
        Appointment.treat_id == treat.c.treat_id,
        treat.c.patient_id == patient_id
    ).all()

    # print(f"stmt = {stmt}, type = {type(stmt)}")

    return appointments_schema.dump(stmt)

##################################################

@app.route("/appointments/doctors/<int:doc_id>")
def get_doctor_appointments(doc_id):
    stmt = db.session.query(Appointment).join(treat).filter(
        Appointment.treat_id == treat.c.treat_id,
        treat.c.doc_id == doc_id
    )  # .all()

    # print(f"stmt = {stmt}, type = {type(stmt)}")

    return appointments_schema.dump(stmt)
