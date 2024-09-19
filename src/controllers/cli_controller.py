from init import db, bcrypt
from main import app
from models.models import Patient, Doctor, Treatment, Appointment, Log

##################################################

# drop tables
@app.cli.command("drop")
def drop_tables():
    """_summary_
    """
    db.drop_all()
    print("Tables droppped.")

##################################################

# create tables
@app.cli.command("create")
def create_tables():
    """_summary_
    """
    db.create_all()
    print("Tables created.")

##################################################

# seed tables with patients, doctors, treatments, logs and appointments
@app.cli.command("seed")
def seed_tables():
    """_summary_
    """
    
    
    # seed patients
    patients = [
        Patient(
            name="Joel von Treifeldt",
            email="joel@email.com",
            password="password",
            dob="1900-01-01",
            sex="male",
            is_admin=True
        ),
        Patient(
            name="Marie Curie",
            email="Marie@email.com",
            password="password",
            dob="1867-11-07",
            sex="female"
        ),
        Patient(
            name="Erwin Schrodinger",
            email="erwin@schromail.com",
            password="password",
            dob="1887-08-12",
            sex="male"
        ),
        Patient(
            name="Sue Jackson",
            email="sue@email.com",
            password="password",
            dob="1900-01-01",
            sex="female"
        )
    ]
    
    # add seeded patients to database session and commit
    db.session.add_all(patients)
    db.session.commit()


    # seed doctors
    doctors = [
        Doctor(
            name="Jane Smyth",
            email="jane@email.com",
            password="password",
        ),
        Doctor(
            name="Fred Hollows",
            email="fred@email.com",
            password="password",
        ),
        Doctor(
            name="Cleopatra",
            email="cleo@email.com",
            password="password",
        ),
        Doctor(
            name="John Smith",
            email="john@email.com",
            password="password",
        )
    ]
    
    # add seeded doctors to database session and commit
    db.session.add_all(doctors)
    db.session.commit()


    # seed treatments
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
            patient = patients[1],
            doctor = doctors[0],
            start_date="1999-01-01",
            end_date="2024-03-04"
        )
    ]
    
    # add seeded treatments to database session and commit
    db.session.add_all(treatments)
    db.session.commit()


    # seed appointments
    appointments = [
        Appointment(
            datetime="2000-12-12",
            place="Frog's Hollow Medical Centre",
            cost="100",
            status="Completed",
            treatment_id=treatments[0].treatment_id  # should change this so that i'm querying treatment for a particular patient and doctor combo
        ),
        Appointment(
            datetime="1999-06-13",
            place="Spring Hill Medical Centre",
            cost="206",
            status="Completed",
            treatment_id=treatments[0].treatment_id  # should change this so that i'm querying treatment for a particular patient and doctor combo
        ),
        Appointment(
            datetime="2024-10-01",
            place="UQ Medical Centre",
            cost="58",
            status="Scheduled",
            treatment_id=treatments[1].treatment_id  # should change this so that i'm querying treatment for a particular patient and doctor combo
        ),
        Appointment(
            datetime="2023-10-01",
            place="UQ Medical Centre",
            cost="77",
            status="Completed",
            treatment_id=treatments[1].treatment_id  # should change this so that i'm querying treatment for a particular patient and doctor combo
        ),
        Appointment(
            datetime="1463-09-02",
            place="London Medical Centre",
            cost="2",
            status="Completed",
            treatment_id=treatments[2].treatment_id  # should change this so that i'm querying treatment for a particular patient and doctor combo
        )
    ]
    
    # add seeded appointments to database session and commit
    db.session.add_all(appointments)
    db.session.commit()
    

    
    # seed logs
    logs = [
        Log(
            date = "2024-09-16",
            symptom = "API-induced headache",
            patient_id = 1
        ),
        Log(
            date = "1724-09-16",
            symptom = "tuberculosis",
            duration = "3 months",
            patient_id = 3
        ),
        Log(
            date = "1111-11-11",
            symptom = "death",
            duration = "a while now",
            severity = "severe",
            patient_id = 2
        ),
        Log(
            date = "2023-12-3",
            symptom = "Sore spirit",
            severity = "mild",
            patient_id = 2
        )
    ]
    

    # add seeded logs to database session and commit
    db.session.add_all(logs)
    db.session.commit()
    

    # print success message
    print("Tables seeded.")

##################################################

