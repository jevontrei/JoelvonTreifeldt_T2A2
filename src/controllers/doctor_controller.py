from init import db
from models import Doctor, doctor_schema, doctors_schema
 
from flask import jsonify, request, Blueprint


##################################################


doctors_bp = Blueprint("doctors", __name__, url_prefix="/doctors")
# doctors_bp.register_blueprint(comments_bp)


##################################################


# @app.route("/doctors/")
@doctors_bp.route("/")
def get_all_doctors():
    # create SQL statement
    # SELECT * FROM doctors ORDER BY ...?;
    stmt = db.select(Doctor).order_by(Doctor.name)
    print(stmt)

    doctors = db.session.scalars(stmt)
    
    return doctors_schema.dump(doctors)


##################################################


# @app.route("/doctors/<int:doctor_id>")
@doctors_bp.route("/<int:doctor_id>")
def get_a_doctor(doctor_id):
    # create SQL statement
    
    # SELECT * FROM doctos WHERE ... = doctor_id?;
    
    stmt = db.select(Doctor).filter_by(doctor_id=doctor_id)
    print(stmt)

    doctor = db.session.scalar(stmt)
    
    return doctor_schema.dump(doctor)


##################################################


# @app.route("/doctors/", methods=["POST"])
@doctors_bp.route("/", methods=["POST"])
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


# @app.route("/doctors/<int:doctor_id>", methods=["PUT", "PATCH"])
@doctors_bp.route("/<int:doctor_id>", methods=["PUT", "PATCH"])
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


# @app.route("/doctors/<int:doctor_id>", methods=["DELETE"])
@doctors_bp.route("/<int:doctor_id>", methods=["DELETE"])
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


##################################################
