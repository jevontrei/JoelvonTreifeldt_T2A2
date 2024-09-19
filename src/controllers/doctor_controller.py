from init import db
# from models.doctor import Doctor, doctor_schema, doctors_schema
from models.models import Doctor, doctor_schema, doctors_schema
from main import app
from flask import request


##################################################

@app.route("/doctors/")
def get_all_doctors():
    # create SQL statement
    # SELECT * FROM doctors ORDER BY ...?;
    stmt = db.select(Doctor).order_by(Doctor.name)
    doctors = db.session.scalars(stmt)
    return doctors_schema.dump(doctors)

##################################################


@app.route("/doctors/<int:doc_id>")
def get_a_doctor(doc_id):
    # create SQL statement
    # SELECT * FROM doctos WHERE ... = doc_id?;
    stmt = db.select(Doctor).filter_by(doc_id=doc_id)
    doctor = db.session.scalar(stmt)
    return doctor_schema.dump(doctor)

##################################################


@app.route("/doctors/", methods=["POST"])
def create_doctor():
    body_data = request.get_json()
    # remember to validate input!
    doctor = Doctor(
        name=body_data.get("name"),
        email=body_data.get("email"),
        password=body_data.get("password")
    )

    db.session.add(doctor)
    db.session.commit()

    return doctor_schema.dump(doctor), 201

##################################################


@app.route("/doctors/<int:doc_id>", methods=["PUT", "PATCH"])
def update_doctor(doc_id):
    body_data = request.get_json()
    # create SQL statement
    # SELECT * FROM doctors WHERE ... = doc_id?;
    stmt = db.select(Doctor).filter_by(doc_id=doc_id)
    doctor = db.session.scalar(stmt)
    if doctor:
        doctor.name = body_data.get("name") or doctor.name
        doctor.email = body_data.get("email") or doctor.email
        doctor.password = body_data.get("password") or doctor.password
        # patients and appointments? no, do this through treatment and appts, respectively?

        db.session.commit()
        return doctor_schema.dump(doctor)
    else:
        return {"error": f"Doctor {doc_id} not found."}  # , 404

##################################################


@app.route("/doctors/<int:doc_id>", methods=["DELETE"])
def delete_doctor(doc_id):
    # create SQL statement
    # SELECT * FROM doctors WHERE doc_id = doc_id?;
    stmt = db.select(Doctor).filter_by(doc_id=doc_id)
    doctor = db.session.scalar(stmt)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        return {"message": f"Doctor {doc_id} deleted."}  # , 200
    else:
        return {"error": f"Sorry, doctor {doc_id} not found."}  # , 404?

##################################################
