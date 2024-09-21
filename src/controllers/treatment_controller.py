from init import db
from models import Treatment, treatment_schema, treatments_schema
from utils import authorise_as_admin

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required


#####################################################

treatments_bp = Blueprint("treatments", __name__, url_prefix="/treatments")

#####################################################

# http://localhost:5000/treatments/
@treatments_bp.route("/")
@jwt_required()
def get_all_treatments():
    """
    Get all treatments

    Returns:
        _type_: _description_
    """
    # create SQL statement
    # SELECT * FROM treatments;
    stmt = db.select(Treatment)
    print(stmt)

    # execute statement, store in an iterable object
    treatments = db.session.scalars(stmt)
    
    # serialise object to JSON, return it
    return treatments_schema.dump(treatments)


#####################################################

# http://localhost:5000/treatments/<int:treatment_id>
@treatments_bp.route("/<int:treatment_id>")
@jwt_required()
def get_a_treatment(treatment_id):
    """
    Get a specific treatment using the id

    Args:
        treatment_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # create SQL statement
    # SELECT * FROM treatments WHERE treatment_id=treatment_id ... ?;
    stmt = db.select(Treatment).filter_by(treatment_id=treatment_id)
    print(stmt)
    
    treatment = db.session.scalar(stmt)
    
    return treatment_schema.dump(treatment)

#####################################################

# is this URL backwards?

@treatments_bp.route("/patients/<int:patient_id>")
@jwt_required()
def get_patient_treatments(patient_id):
    """
    Get all treatment details for a particular patient

    Args:
        patient_id (_type_): _description_
    """
    # create SQL statement
    # SELECT * FROM treatments WHERE patient_id=patient_id ...?
    stmt = db.select(Treatment).filter_by(patient_id=patient_id)
    print(stmt)
    
    treatments = db.session.scalars(stmt)
    
    return treatments_schema.dump(treatments)

#####################################################

# is this URL backwards?

@treatments_bp.route("/doctors/<int:doctor_id>")
@jwt_required()
def get_doctor_treatments(doctor_id):
    """
    Get all treatment details for a particular doctor

    Args:
        doctor_id (_type_): _description_
    """
    # create SQL statement
    # SELECT * FROM treatments WHERE doctor_id=doctor_id ...?
    
    stmt = db.select(Treatment).filter_by(doctor_id=doctor_id)
    print(stmt)

    treatments = db.session.scalars(stmt)
    
    return treatments_schema.dump(treatments)

#####################################################


@treatments_bp.route("/", methods=["POST"])
@jwt_required()
def create_treatment():
    """
    Add a new treatment between doctor and patient

    Args:
        patient_id (_type_): _description_
        doctor_id (_type_): _description_
    """
    # fetch data, deserialise it, store in variable
    body_data = request.get_json()
    
    # remember to validate input! especially FKs
    # define new instance of Treatment class
    treatment = Treatment(
        patient_id=body_data.get("patient_id"),
        doctor_id=body_data.get("doctor_id"),
        start_date=body_data.get("start_date"),
        end_date=body_data.get("end_date")
    )
    
    db.session.add(treatment)
    db.session.commit()

    return treatment_schema.dump(treatment), 201

#####################################################


@treatments_bp.route("/<int:treatment_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_treatment(treatment_id):
    
    # still need to authorise!!
    
    body_data = request.get_json()
    
    # create SQL statement
    # SELECT * FROM treatments WHERE treatment_id = treatment_id ... ?;
    stmt = db.select(Treatment).filter_by(treatment_id=treatment_id)
    print(stmt)
    
    # execute ...
    treatment = db.session.scalar(stmt)
    
    # if treatment exists, apply ...
    if treatment:
        treatment.patient_id = body_data.get("patient_id") or treatment.patient_id
        treatment.doctor_id = body_data.get("doctor_id") or treatment.doctor_id
        treatment.start_date = body_data.get("start_date") or treatment.start_date
        treatment.end_date = body_data.get("end_date") or treatment.end_date

        db.session.commit()
        
        return treatment_schema.dump(treatment)
    
    else:
        return jsonify({"error": f"Treatment {treatment_id} not found."}), 404
    
#####################################################


@treatments_bp.route("/<int:treatment_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_treatment(treatment_id):
    
    # create SQL statement
    # SELECT ?
    stmt = db.select(Treatment).filter_by(treatment_id=treatment_id)
    print(stmt)
    
    # execute statement and ...
    treatment = db.session.scalar(stmt)
    
    # if treatment exists:
    if treatment:
        db.session.delete(treatment)
        db.session.commit()
        return jsonify({"message": f"Treatment {treatment_id} deleted."})  # , 200
    
    else:
        return jsonify({"error": f"Treatment {treatment_id} not found."}), 404