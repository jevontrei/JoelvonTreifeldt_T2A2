from init import db, bcrypt
from models import Patient, Doctor, Treatment, Appointment, Log

from flask import Blueprint

##################################################

# change this, remove "db", save time typing?!
# Create blueprint with URL prefix
db_commands = Blueprint(
    "db", 
    __name__
)

##################################################

@db_commands.cli.command("drop")
def drop_tables():
    """Drop all tables.
    """
    
    # Delete all tables from the database (even if FK constraints are present? how to do this?)
    db.drop_all()
    
    print("Tables dropped.")

##################################################

@db_commands.cli.command("create")
def create_tables():
    """Create all tables.
    """
    
    db.create_all()
    
    print("Tables created.")

##################################################

@db_commands.cli.command("seed")
def seed_tables():
    """Seed tables with details for patients, doctors, treatments, logs and appointments.
    """
    
    # Seed patients
    patients = [
        Patient(
            name="Joel von Treifeldt",
            email="joel@email.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8"),
            dob="1900-01-01",
            sex="male",
            is_admin=True
        ),
        Patient(
            name="Marie Curie",
            email="marie@email.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8"),
            dob="1867-11-07",
            sex="female",
            is_admin=True
        ),
        Patient(
            name="Erwin Schrodinger",
            email="erwin@schromail.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8"),
            dob="1887-08-12",
            sex="male"
        ),
        Patient(
            name="Mary Magdalene",
            email="mary@magmail.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8"),
            dob="1900-01-01",
            sex="female"
        )
    ]
    
    # Add seeded patients to session and commit changes to database
    db.session.add_all(patients)
    db.session.commit()

    # Seed doctors
    doctors = [
        Doctor(
            name="Cardi B",
            email="cardi@hipmail.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8")
        ),
        Doctor(
            name="Fred Hollows",
            email="fred@eyemail.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8"),
            specialty="optometry"
        ),
        Doctor(
            name="Cleopatra",
            email="cleo@email.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8"),
            sex="female",
            is_admin=True
        ),
        Doctor(
            name="Socrates",
            email="socrates@email.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8"),
            sex="male",
            specialty="divination",
            is_admin=True
        ),
        Doctor(
            name="Steve Jobs",
            email="steve@applemail.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8")
        )
    ]
    
    # Add seeded doctors to session and commit changes to database
    db.session.add_all(doctors)
    db.session.commit()

    # Seed treatments
    treatments = [
        Treatment(
            patient = patients[0],
            doctor = doctors[0],
            start_date="2024-01-01",
            end_date="2024-01-02"
        ),
        Treatment(
            patient = patients[0],
            doctor = doctors[1],
            start_date="2023-11-21"
        ),
        Treatment(
            patient = patients[3],
            doctor = doctors[2],
            start_date="1923-03-01"
        ),
        Treatment(
            patient = patients[3],
            doctor = doctors[3],
            start_date="1823-11-21"
        ),
        Treatment(
            patient = patients[1],
            doctor = doctors[0],
            start_date="1999-01-01",
            end_date="2024-03-04"
        )
    ]
    
    # Add seeded treatments to session and commit changes to database
    db.session.add_all(treatments)
    db.session.commit()

    # Seed appointments
    appointments = [
        Appointment(
            date="2000-12-12",
            time="07:00",
            place="Frog's Hollow Medical Centre",
            cost="100",
            status="Completed",
            treatment_id=treatments[0].treatment_id  # should change these so that i'm querying treatment for a particular patient and doctor combo?
        ),
        Appointment(
            date="1999-06-13",
            time="12:00",
            place="Spring Hill Medical Centre",
            cost="206",
            status="Completed",
            treatment_id=treatments[0].treatment_id
        ),
        Appointment(
            date="1989-06-13",
            time="16:00",
            place="Spring Hill Medical Centre",
            cost="99",
            status="Cancelled",
            notes="general checkup",
            treatment_id=treatments[0].treatment_id
        ),
        Appointment(
            date="2024-12-01",
            time="11:30",
            place="UQ Medical Centre",
            cost="58",
            status="Scheduled",
            treatment_id=treatments[1].treatment_id
        ),
        Appointment(
            date="2025-06-08",
            time="09:00",
            place="UQ Medical Centre",
            cost="52",
            status="Scheduled",
            notes="yearly mental health appt",
            treatment_id=treatments[2].treatment_id
        ),
        Appointment(
            date="2023-10-01",
            time="13:00",
            place="UQ Medical Centre",
            cost="77",
            status="Completed",
            treatment_id=treatments[1].treatment_id
        ),
        Appointment(
            date="1463-09-02",
            time="12:00",
            place="London Medical Centre",
            cost="32",
            status="Completed",
            notes="blood test",
            treatment_id=treatments[2].treatment_id
        ),
        Appointment(
            date="1463-09-11",
            time="14:30",
            place="London Medical Centre",
            cost="21",
            status="Completed",
            notes="follow-up for blood test",
            treatment_id=treatments[2].treatment_id
        )
    ]
    
    # Add seeded appointments to session and commit changes to database
    db.session.add_all(appointments)
    db.session.commit()
    
    # Seed logs
    logs = [
        Log(
            date = "2024-09-16",
            notes = "API-induced headache",
            patient_id = 1
        ),
        Log(
            date = "1724-09-16",
            notes = "coughing, reminds me of the time I had tuberculosis; it's been 3 months now",
            patient_id = 3
        ),
        Log(
            date = "1111-11-11",
            notes = "death; a while now; severe",
            patient_id = 2
        ),
        Log(
            date = "2222-12-12",
            notes = "started taking antibiotics for a chest infection",
            patient_id = 4
        ),
        Log(
            date = "2222-12-30",
            notes = "finished antibiotics course; feeling better",
            patient_id = 4
        ),
        Log(
            date = "4442-12-30",
            notes = "my Neuralink fell out",
            patient_id = 1
        ),
        Log(
            date = "2023-12-3",
            notes = "Sore spirit",
            patient_id = 2
        )
    ]
    
    # Add seeded logs to session and commit changes to database
    db.session.add_all(logs)
    db.session.commit()

    # Print success message
    print("Tables seeded.")
