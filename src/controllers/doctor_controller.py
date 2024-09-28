from init import db
from models import Doctor, doctor_schema, doctors_schema, Appointment, appointments_schema, Treatment, treatments_schema
from utils import authorise_as_admin


from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

# delet:
from sqlalchemy.exc import IntegrityError


##################################################

# Create blueprint with URL prefix
doctors_bp = Blueprint(
    "doctors",
    __name__,
    url_prefix="/doctors"
)

##################################################

# http://localhost:5000/doctors/


@doctors_bp.route("/")
@jwt_required()
# Authorise as admin since serialised doctor info includes all sensitive treatment details
@authorise_as_admin
def get_all_doctors():
    """Fetch details for all doctors.

    Returns:
        JSON: All doctor details, serialised.
    """
    try:
        # Create SQLAlchemy query statement:
        # SELECT *
        # FROM doctors
        # ORDER BY doctors.name;
        stmt = db.select(
            Doctor
        ).order_by(
            Doctor.name
        )

        # ... ? fetchall() prevents returning an empty list/dict
        doctors = db.session.scalars(stmt).fetchall()

        # Guard clause; return error if no doctors exist
        if not doctors:
            return jsonify(
                {"error": "No doctors found."}
            ), 404

        # Return doctor objects serialised according to the doctors schema
        return doctors_schema.dump(doctors)

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


##################################################

# http://localhost:5000/doctors/<int:doctor_id>
@doctors_bp.route("/<int:doctor_id>")
@jwt_required()
# Authorise as admin since serialised doctor info includes all sensitive treatment details
@authorise_as_admin
def get_a_doctor(doctor_id):
    """Fetch details of a particular doctor.

    Args:
        doctor_id (int): Doctor primary key.

    Returns:
        JSON: Serialised details for one doctor.
    """
    try:
        # Create SQLAlchemy query statement:
        # SELECT *
        # FROM doctors
        # WHERE doctors.doctor_id = :doctor_id_1;
        stmt = db.select(
            Doctor
        ).filter_by(
            doctor_id=doctor_id
        )

        # Connect to database session, execute statement, store resulting value
        doctor = db.session.scalar(stmt)

        # Guard clause; return error if doctor doesn't exist
        if not doctor:
            return jsonify(
                {"error": f"Doctor {doctor_id} not found."}
            ), 404

        # # Return doctor object serialised according to the doctor schema
        return doctor_schema.dump(doctor)

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


##################################################

# http://localhost:5000/doctors/<int:doctor_id>/appointments/
@doctors_bp.route("/<int:doctor_id>/appointments/")
@jwt_required()
# This is a high-level endpoint that should be accessible to admins only
# In future, build a doctor auth decorator with an early exit for admins
@authorise_as_admin
def get_doctor_appointments(doctor_id):
    """Get all appointments for a particular doctor.

    Args:
        doctor_id (int): Doctor primary key.

    Returns:
        JSON: All appointment details for the given doctor.
    """

    try:
        # Create SQLAlchemy query statement:
        # SELECT *
        # FROM appointments
        # JOIN treatments
        # ON treatments.treatment_id = appointments.treatment_id
        # WHERE treatments.doctor_id = :doctor_id_1
        # ORDER BY appointments.date, appointments.time;
        stmt = db.select(
            Appointment
        ).join(
            Treatment
        ).filter(
            Treatment.doctor_id == doctor_id
        ).order_by(
            Appointment.date, Appointment.time
        )

        # Execute statement using scalars()
        # Use fetchall() to return all resulting values, which also avoids returning an empty list/dict for queries for nonexistent doctors (e.g. doctor_id=99999)
        appointments = db.session.scalars(stmt).fetchall()

        # Guard clause; return error if no appointments exist
        if not appointments:
            return jsonify(
                {"error": f"No appointments found for doctor {doctor_id}."}
            ), 404

        # Return appointment objects serialised according to the appointments schema
        return appointments_schema.dump(appointments)

    # In case a queried-for entity is nonexistent or has been deleted
    except UnboundLocalError as e:
        return jsonify(
            {"error": str(e)}
        ), 404

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


#####################################################

# http://localhost:5000/doctors/<int:doctor_id>/treatments/
@doctors_bp.route("<int:doctor_id>/treatments/")
@jwt_required()
# This is a high-level endpoint that should be accessible to admins only
# In future, build a doctor auth decorator with an early exit for admins
@authorise_as_admin
def get_doctor_treatments(doctor_id):
    """Get all treatment details for a particular doctor

    Args:
        doctor_id (int): Doctor primary key.

    Returns:
        JSON: All treatment details for the given doctor.
    """

    try:
        # Create SQLAlchemy query statement:
        # SELECT *
        # FROM treatments
        # WHERE treatments.doctor_id = :doctor_id_1
        # ORDER BY treatments.start_date;
        stmt = db.select(
            Treatment
        ).filter_by(
            doctor_id=doctor_id
        ).order_by(
            Treatment.start_date
        )

        treatments = db.session.scalars(stmt).fetchall()

        # Guard clause; return error if no treatments exist
        if not treatments:
            return jsonify(
                {"error": f"No treatments found for doctor {doctor_id}."}
            ), 404

        # Return treatment objects serialised according to the treatments schema
        return treatments_schema.dump(treatments)

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


##################################################

# http://localhost:5000/doctors/<int:doctor_id>
@doctors_bp.route("/<int:doctor_id>", methods=["PUT", "PATCH"])
@jwt_required()
# This is a high-level endpoint that should be accessible to admins only
# In future, build a doctor auth decorator with an early exit for admins
@authorise_as_admin
def update_doctor(doctor_id):
    """Edit details for a particular doctor.

    Args:
        doctor_id (int): Doctor primary key.

    Returns:
        JSON: Updated details serialised according to the doctor schema.
    """
    try:
        # Fetch body of HTTP request
        body_data = request.get_json()

        # Create SQLAlchemy query statement:
        # SELECT *
        # FROM doctors
        # WHERE doctors.doctor_id = :doctor_id_1;
        stmt = db.select(Doctor).filter_by(doctor_id=doctor_id)

        # Connect to database session, execute statement, store resulting value
        doctor = db.session.scalar(stmt)

        # Guard clause; return error if doctor doesn't exist
        if not doctor:
            return jsonify(
                {"error": f"Doctor {doctor_id} not found."}
            ), 404

        # can i do this more efficiently with kwargs?
        doctor.name = body_data.get("name") or doctor.name
        doctor.email = body_data.get("email") or doctor.email
        # use pop() instead?  # .pop() increases secruity by removing password
        doctor.password = body_data.get("password") or doctor.password
        # patients and appointments? no, do this through treatments and appointments, respectively?

        # Commit changes to database
        db.session.commit()

        # Return updated doctor object serialised according to the doctor schema
        return doctor_schema.dump(doctor)

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


##################################################

# http://localhost:5000/doctors/<int:doctor_id>
@doctors_bp.route("/<int:doctor_id>", methods=["DELETE"])
@jwt_required()
# This is a high-level endpoint that should be accessible to admins only
# In future, build a doctor auth decorator with an early exit for admins
@authorise_as_admin
def delete_doctor(doctor_id):
    """Delete a doctor. WARNING: Not recommended. This action is destructive and will prevent anyone from viewing ANY treatment or appointment details associated with any related treatment ID. All related appointments will be deleted. The @authorise_treatment_participant decorator will not be functional for appointment GET requests. An admin should archive all related treatment and appointment details (especially notes) in the patient's log before deleting doctor.

    Args:
        doctor_id (int): Doctor primary key.

    Returns:
        JSON: Success message.
    """
    try:
        # Create SQLAlchemy query statement:
        # SELECT *
        # FROM doctors
        # WHERE doctors.doctor_id = :doctor_id_1;
        stmt = db.select(Doctor
                         ).filter_by(
            doctor_id=doctor_id
        )

        # Connect to database session, execute statement, store resulting value
        doctor = db.session.scalar(stmt)

        # Guard clause; return error if doctor doesn't exist
        if not doctor:
            return jsonify(
                {"error": f"Doctor {doctor_id} not found."}
            ), 404

        # Delete doctor and commit changes to database
        db.session.delete(doctor)
        db.session.commit()

        # Return serialised success message
        return jsonify(
            {"message": f"Doctor {doctor_id} deleted."}
        )

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500
