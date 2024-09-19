from init import db
from models.models import Treatment, treatment_schema, treatments_schema
from main import app
from flask import request


#####################################################

@app.route("/treatments/")
def get_all_treatments():
    """
    Get all treatments

    Returns:
        _type_: _description_
    """
    # create SQL statement
    # SELECT * FROM treatment;
    stmt = db.select(Treatment)
    
    # execute statement, store in an iterable object
    treatments = db.session.scalars(stmt)
    
    # serialise object to JSON, return it
    return treatments_schema.dump(treatments)


#####################################################

@app.route("/treatments/<int:treatment_id>")
def get_a_treatment(treatment_id):
    """
    Get a specific treatment

    Args:
        treatment_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # create SQL statement
    # SELECT * FROM treatment WHERE treatment_id=treatment_id ... ?;
    stmt = db.select(Treatment).filter_by(treatment_id=treatment_id)
    
    treatment = db.session.scalar(stmt)
    
    return treatment_schema.dump(treatment)

#####################################################

@app.route("/treatments/patients/<int:patient_id>")
def get_patient_treatments(patient_id):
    """
    Get all treatment details for a particular patient

    Args:
        patient_id (_type_): _description_
    """
    # create SQL statement
    # SELECT * FROM treatment WHERE patient_id=patient_id ...?
    stmt = db.select(Treatment).filter_by(patient_id=patient_id)
    
    treatments = db.session.scalars(stmt)
    
    return treatments_schema.dump(treatments)

#####################################################


@app.route("/treatments/doctors/<int:doc_id>")
def get_doctor_treatments(doc_id):
    """
    Get all treatment details for a particular doctor

    Args:
        doc_id (_type_): _description_
    """
    # create SQL statement
    # SELECT * FROM treatment WHERE doc_id=doc_id ...?
    
    stmt = db.select(Treatment).filter_by(doc_id=doc_id)
    
    treatments = db.session.scalars(stmt)
    
    return treatments_schema.dump(treatments)

#####################################################


@app.route("/treatments/", methods=["POST"])
def create_treatment():
    """
    Add a new treatment between doctor and patient

    Args:
        patient_id (_type_): _description_
        doc_id (_type_): _description_
    """
    # fetch data, deserialise it, store in variable
    body_data = request.get_json()
    
    # remember to validate input!
    # define new instance of Treatment class
    treatment = Treatment(
        patient_id=body_data.get("patient_id"),
        doc_id=body_data.get("doc_id"),
        start_date=body_data.get("start_date"),
        end_date=body_data.get("end_date")
    )
    
    db.session.add(treatment)
    db.session.commit()

    return treatment_schema.dump(treatment), 201

#####################################################


@app.route("/treatments/<int:treatment_id>", methods=["PUT", "PATCH"])
def update_treatment(treatment_id):
    
    # still need to authorise!!
    
    body_data = request.get_json()
    
    # create SQL statement
    # SELECT * FROM treatment WHERE treatment_id = treatment_id ... ?;
    stmt = db.select(Treatment).filter_by(treatment_id=treatment_id)
    
    # execute ...
    treatment = db.session.scalar(stmt)
    
    # if treatment exists, apply ...
    if treatment:
        treatment.patient_id = body_data.get("patient_id") or treatment.patient_id
        treatment.doc_id = body_data.get("doc_id") or treatment.doc_id
        treatment.start_date = body_data.get("start_date") or treatment.start_date
        treatment.end_date = body_data.get("end_date") or treatment.end_date

        db.session.commit()
        
        return treatment_schema.dump(treatment)
    
    else:
        return {"error": f"Treatment {treatment_id} not found."}  # , 404
    
#####################################################


@app.route("/treatments/<int:treatment_id>", methods=["DELETE"])
def delete_treatment(treatment_id):
    
    # still need to authorise!!
    
    # create SQL statement
    stmt = db.select(Treatment).filter_by(treatment_id=treatment_id)
    
    # execute statement and ...
    treatment = db.session.scalar(stmt)
    
    # if treatment exists:
    if treatment:
        db.session.delete(treatment)
        db.session.commit()
        return {"message": f"Treatment {treatment_id} deleted."}  # , 200
    
    else:
        return {"error": f"Sorry, Treatment {treatment_id} not found."}  # , 404?