from init import db
from models import Patient, patient_schema, patients_schema, Appointment, appointments_schema, Treatment, treatments_schema
from utils import authorise_as_admin

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

        patients = db.session.scalars(stmt).fetchall()

        # Guard clause; return error if no patients exist
        if not patients:
            return jsonify(
                {"error": "No patients found."}
            ), 404

        # Return patient objects serialised according to the patients schema
        return patients_schema.dump(patients)

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

# http://localhost:5000/patients/<int:patient_id>
@patients_bp.route("/<int:patient_id>")
@jwt_required()
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

# http://localhost:5000/patients/<int:patient_id>/appointments/
@patients_bp.route("/<int:patient_id>/appointments/")
@jwt_required()
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

# http://localhost:5000/patients/<int:patient_id>/treatments/
@patients_bp.route("/<int:patient_id>/treatments/")
@jwt_required()
# justify why i chose this particular auth decorator
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

        treatments = db.session.scalars(stmt).fetchall()

        # Guard clause; return error if no treatments exist
        if not treatments:
            return jsonify(
                {"error": f"No treatments found for patient {patient_id}."}
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

# http://localhost:5000/patients/<int:patient_id>
@patients_bp.route("/<int:patient_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_patient(patient_id):
    """Edit a patient's details.

    Args:
        patient_id (int): Patient primary key.

    Returns:
        JSON: Updated and serialised patient details.
    """

    try:

        # Fetch ...?
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
        # use pop() instead?  # .pop() increases secruity by removing password
        patient.password = body_data.get("password") or patient.password
        patient.dob = body_data.get("dob") or patient.dob
        patient.sex = body_data.get("sex") or patient.sex
        patient.is_admin = body_data.get("is_admin") or patient.is_admin
        # logs and doctors? no, do this through logs and treatments, respectively?

        # Commit changes to database
        db.session.commit()

        # Return updated patient object serialised according to the patient schema
        return patient_schema.dump(patient)

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

# http://localhost:5000/patients/<int:patient_id>
@patients_bp.route("/<int:patient_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_patient(patient_id):
    """Delete a patient.

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

    # In case ... ?
    # except ? as e:
    #     return jsonify(
    #         {"error": "?"}
    #     ), ?00

    except Exception as e:
        return jsonify(
            {"error": f"Unexpected error: {e}."}
        ), 500
