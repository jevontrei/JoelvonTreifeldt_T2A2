from init import db
from models import Patient, patient_schema, patients_schema, Appointment, appointments_schema, Treatment, treatments_schema
from utils import authorise_as_admin, authorise_treatment_participant

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

##################################################

# Create blueprint with URL prefix
patients_bp = Blueprint(
    "patients",
    __name__,
    url_prefix="/patients"
)

##################################################

# http://localhost:5000/patients/


@patients_bp.route("/")
@jwt_required()
# This is a high-level endpoint that should be accessible to admins only
@authorise_as_admin
def get_all_patients():
    """Get details for all patients.

    Returns:
        JSON: Serialised list of patient details.
    """
    try:

        # Create SQLAlchemy query statement:
        # SELECT patients.patient_id, patients.name, patients.email, patients.password, patients.dob, patients.sex, patients.is_admin
        # FROM patients
        # ORDER BY patients.name;
        stmt = db.select(
            Patient
        ).order_by(
            Patient.name
        )

        # Execute statement, fetch resulting values
        patients = db.session.scalars(stmt).fetchall()

        # Guard clause; return error if no patients exist
        if not patients:
            return jsonify(
                {"error": "No patients found."}
            ), 404

        # Return patient objects serialised according to the patients schema
        return patients_schema.dump(patients)

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


##################################################

# http://localhost:5000/patients/<int:patient_id>
@patients_bp.route("/<int:patient_id>")
@jwt_required()
# This is a high-level endpoint that should be accessible to admins only
# In future, build a patient auth decorator with an early exit for admins
# Doctors can simply view patient logs instead
@authorise_as_admin
def get_a_patient(patient_id):
    """Get a particular patient's details.

    Args:
        patient_id (int): Patient primary key.

    Returns:
        JSON: Serialised patient details.
    """
    try:
        # Create SQLAlchemy query statement:
        # SELECT patients.patient_id, patients.name, patients.email, patients.password, patients.dob, patients.sex, patients.is_admin
        # FROM patients
        # WHERE patients.patient_id = :patient_id_1;
        stmt = db.select(
            Patient
        ).filter_by(
            patient_id=patient_id
        )

        # Connect to database session, execute statement, store resulting value
        patient = db.session.scalar(stmt)

        # Guard clause; return error if patient doesn't exist
        if not patient:
            return jsonify(
                {"error": f"Patient {patient_id} not found."}
            ), 404

        # Return patient object serialised according to the patient schema
        return patient_schema.dump(patient)

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


##################################################

# http://localhost:5000/patients/<int:patient_id>/appointments/
@patients_bp.route("/<int:patient_id>/appointments/")
@jwt_required()
# This is a high-level endpoint that should be accessible to admins only
# In future, build a patient auth decorator with an early exit for admins
@authorise_as_admin
def get_patient_appointments(patient_id):
    """Get all appointments for a particular patient.

    Args:
        patient_id (int): Patient primary key.

    Returns:
        JSON: a list of appointment details for the given patient.
    """
    try:
        # Create SQLAlchemy query statement:
        # SELECT appointments.appt_id, appointments.date, appointments.time, appointments.place, appointments.cost, appointments.status, appointments.treatment_id
        # FROM appointments
        # JOIN treatments
        # ON treatments.treatment_id = appointments.treatment_id
        # WHERE treatments.patient_id = :patient_id_1
        # ORDER BY appointments.date, appointments.time;
        stmt = db.select(
            Appointment
        ).join(
            Treatment
        ).filter(
            Treatment.patient_id == patient_id
        ).order_by(
            Appointment.date, Appointment.time
        )

        # Execute statement using scalars(), and fetch all resulting values
        appointments = db.session.scalars(stmt).fetchall()

        # Guard clause; return error if no appointments exist
        if not appointments:
            return jsonify(
                {"error": f"No appointments found for patient {patient_id}."}
            ), 404

        # Return appointment objects serialised according to the appointments schema
        return appointments_schema.dump(appointments)

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


#####################################################

# http://localhost:5000/patients/<int:patient_id>/treatments/
@patients_bp.route("/<int:patient_id>/treatments/")
@jwt_required()
# This is a high-level endpoint that should be accessible to admins only
# In future, build an appropriate patient/doctor auth decorator with an early exit for admins. The @authorise_treatment_participant decorator is insufficient, e.g. because you don't want your optometrist accessing your psychology treatment details
@authorise_as_admin
def get_patient_treatments(patient_id):
    """Get all treatment details for a particular patient.

    Args:
        patient_id (int): Patient primary key.

    Returns:
        JSON: Treatment details for the given patient.
    """
    try:
        # Create SQLAlchemy query statement:
        # SELECT treatments.treatment_id, treatments.start_date, treatments.end_date, treatments.patient_id, treatments.doctor_id
        # FROM treatments
        # WHERE treatments.patient_id = :patient_id_1;
        stmt = db.select(
            Treatment
        ).filter_by(
            patient_id=patient_id
        )  # .order_by()

        # Execute statement, fetch resulting values
        treatments = db.session.scalars(stmt).fetchall()
        # Guard clause; return error if no treatments exist
        if not treatments:
            return jsonify(
                {"error": f"No treatments found for patient {patient_id}."}
            ), 404

        # Return treatment objects serialised according to the treatments schema
        return treatments_schema.dump(treatments)

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


##################################################

# http://localhost:5000/patients/<int:patient_id>
@patients_bp.route("/<int:patient_id>", methods=["PUT", "PATCH"])
@jwt_required()
# This is a high-level endpoint that should be accessible to admins only
# In future, build a patient auth decorator with an early exit for admins
@authorise_as_admin
def update_patient(patient_id):
    """Edit a patient's details.

    Args:
        patient_id (int): Patient primary key.

    Returns:
        JSON: Updated and serialised patient details.
    """
    try:
        # Fetch body of HTTP request
        body_data = request.get_json()

        # Create SQLAlchemy query statement:
        # SELECT patients.patient_id, patients.name, patients.email, patients.password, patients.dob, patients.sex, patients.is_admin
        # FROM patients
        # WHERE patients.patient_id = :patient_id_1;
        stmt = db.select(
            Patient
        ).filter_by(
            patient_id=patient_id
        )

        # Connect to database session, execute statement, store resulting value
        patient = db.session.scalar(stmt)

        # Guard clause; return error if patient doesn't exist
        if not patient:
            return jsonify(
                {"error": f"Patient {patient_id} not found."}
            ), 404

        patient.name = body_data.get("name") or patient.name
        patient.email = body_data.get("email") or patient.email
        patient.password = body_data.get("password") or patient.password
        patient.dob = body_data.get("dob") or patient.dob
        patient.sex = body_data.get("sex") or patient.sex
        patient.is_admin = body_data.get("is_admin") or patient.is_admin

        # Commit changes to database
        db.session.commit()

        # Return updated patient object serialised according to the patient schema
        return patient_schema.dump(patient)

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500


##################################################

# http://localhost:5000/patients/<int:patient_id>
@patients_bp.route("/<int:patient_id>", methods=["DELETE"])
@jwt_required()
# This is a high-level endpoint that should be accessible to admins only
# In future, build a patient auth decorator with an early exit for admins
@authorise_as_admin
def delete_patient(patient_id):
    """Delete a patient. WARNING: Not recommended. This action is destructive and will delete all treatment and appointment history/details associated with this patient.

    Args:
        patient_id (int): Patient primary key.

    Returns:
        JSON: Success message.
    """

    try:

        # Create SQLAlchemy query statement:
        # SELECT patients.patient_id, patients.name, patients.email, patients.password, patients.dob, patients.sex, patients.is_admin
        # FROM patients
        # WHERE patients.patient_id = :patient_id_1;
        stmt = db.select(
            Patient
        ).filter_by(
            patient_id=patient_id
        )

        # Connect to database session, execute statement, store resulting value
        patient = db.session.scalar(stmt)

        # Guard clause; return error if patient doesn't exist
        if not patient:
            return jsonify(
                {"error": f"Patient {patient_id} not found."}
            ), 404

        # Delete patient and commit changes to database
        db.session.delete(patient)
        db.session.commit()

        # Return serialised success message
        return jsonify(
            {"message": f"Patient {patient_id} deleted."}
        )


    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500

