from init import db
from models.models import Appointment, appointment_schema, appointments_schema, Treatment
from main import app
from flask import request

##################################################

@app.route("/appointments/")
def get_all_appointments():
    """_summary_

    Returns:
        _type_: _description_
    """
    
    # create SQL statement
    # SELECT * FROM appointments;
    stmt = db.select(Appointment)  # .order_by(Appointment.datetime)
    
    appointments = db.session.scalars(stmt)
    
    return appointments_schema.dump(appointments)

##################################################


@app.route("/appointments/<int:appt_id>")
def get_an_appointment(appt_id):
    """_summary_

    Args:
        appt_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # create SQL statement
    # SELECT * FROM appointments WHERE ... = appt_id?;
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)
    
    appointment = db.session.scalar(stmt)
    
    return appointment_schema.dump(appointment)

##################################################

# GOAL: get all appointments for a particular patient

# this is complicated maybe? becuase it's not patient_id, it's treatment_id. how to query treatment using patient_id?

# this was working but not anymore since i renamed auth to treatment?:

@app.route("/appointments/patients/<int:patient_id>")
def get_patient_appointments(patient_id):
    """_summary_

    Args:
        patient_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # create SQL statement
    # SELECT * FROM appointments JOIN? ... WHERE ... ?;
    stmt = db.session.query(Appointment).join(treatment).filter(
        Appointment.treatment_id == treatment.c.treatment_id,
        treatment.c.patient_id == patient_id
    ).all()

    # print(f"stmt = {stmt}, type = {type(stmt)}")

    return appointments_schema.dump(stmt)

##################################################

@app.route("/appointments/doctors/<int:doc_id>")
def get_doctor_appointments(doc_id):
    """_summary_

    Args:
        doc_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # create SQL statement
    # SELECT * FROM appointments JOIN? ... WHERE ... ?;
    stmt = db.session.query(Appointment).join(treatment).filter(
        Appointment.treatment_id == treatment.c.treatment_id,
        treatment.c.doc_id == doc_id
    )  # .all()

    # print(f"stmt = {stmt}, type = {type(stmt)}")

    return appointments_schema.dump(stmt)


##################################################

# @app.route("/appointments/", methods=["POST"])
# def create_appointment():
#     body_data
    

##################################################

@app.route("/appointments/<int:appt_id>", methods=["PUT", "PATCH"])
def update_appointment(appt_id):
    body_data = request.get_json()

    # create SQL statement
    # SELECT * FROM appointments WHERE appointment_id = appointment_id ... ?;
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)
    
    appointment = db.session.scalar(stmt)
    
    if appointment:
        appointment.datetime = body_data.get("datetime") or appointment.datetime
        appointment.place = body_data.get("place") or appointment.place
        appointment.cost = body_data.get("cost") or appointment.cost
        appointment.status = body_data.get("status") or appointment.status
        db.session.commit()
        
        return appointment_schema.dump(appointment)
    
    else:
        return {"error": f"Appointment {appt_id} not found."}, 404
    
    
    

##################################################

@app.route("/appointments/<int:appt_id>", methods=["DELETE"])
def delete_appointment(appt_id):
    # create SQL statement
    # SELECT * FROM appointments WHERE ... ?;
    stmt = db.select(Appointment).filter_by(appt_id=appt_id)
    
    appt = db.session.scalar(stmt)
    
    if appt:
        db.session.delete(appt)
        db.session.commit()
        return {"message": f"Appointment {appt_id} deleted."}
    
    else:
        return {"error": f"Sorry, appointment {appt_id} not found."}  # , 404?

##################################################
