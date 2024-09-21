from init import db
from models import Doctor, doctor_schema, doctors_schema
from utils import authorise_as_admin

 
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

##################################################

doctors_bp = Blueprint("doctors", __name__, url_prefix="/doctors")

##################################################

@doctors_bp.route("/")
# @jwt_required()
def get_all_doctors():
    # create SQL statement
    # SELECT * FROM doctors ORDER BY ...?;
    stmt = db.select(Doctor).order_by(Doctor.name)
    print(stmt)

    doctors = db.session.scalars(stmt)
    
    return doctors_schema.dump(doctors)

##################################################

@doctors_bp.route("/<int:doctor_id>")
# @jwt_required()
def get_a_doctor(doctor_id):
    # create SQL statement
    
    # SELECT * FROM doctos WHERE ... = doctor_id?;
    
    stmt = db.select(Doctor).filter_by(doctor_id=doctor_id)
    print(stmt)

    doctor = db.session.scalar(stmt)
    
    return doctor_schema.dump(doctor)

##################################################

@doctors_bp.route("/<int:doctor_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_doctor(doctor_id):
    
    body_data = request.get_json()
    
    # create SQL statement
    # SELECT * FROM doctors WHERE ... = doctor_id?;
    stmt = db.select(Doctor).filter_by(doctor_id=doctor_id)
    print(stmt)

    doctor = db.session.scalar(stmt)
    
    if doctor:
        doctor.name = body_data.get("name") or doctor.name
        doctor.email = body_data.get("email") or doctor.email
        doctor.password = body_data.get("password") or doctor.password
        # patients and appointments? no, do this through treatments and appointments, respectively?

        db.session.commit()
        
        return doctor_schema.dump(doctor)
    
    else:
        return jsonify({"error": f"Doctor {doctor_id} not found."}), 404

##################################################

@doctors_bp.route("/<int:doctor_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_doctor(doctor_id):
    
    # create SQL statement
    
    # SELECT * FROM doctors WHERE doctor_id = doctor_id?;
    
    stmt = db.select(Doctor).filter_by(doctor_id=doctor_id)
    print(stmt)

    doctor = db.session.scalar(stmt)
    
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({"message": f"Doctor {doctor_id} deleted."})  # , 200
    
    else:
        return jsonify({"error": f"Doctor {doctor_id} not found."}), 404

