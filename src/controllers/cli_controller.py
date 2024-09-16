from init import db, bcrypt
from models.models import Patient, Doctor, treat, Appointment, Log
# from models.doctor import Doctor
from main import app

##################################################


@app.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created.")

##################################################


@app.cli.command("seed")
def seed_tables():
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
            sex="female",
            diagnoses="ADHD"
        )
    ]

    db.session.add_all(patients)

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

    db.session.add_all(doctors)

##########################################################

    # seed treat table? via doctor OR equivalently patients?

    doctors[0].patients.append(patients[0])
    # doctors[0].patients.append(patients[0])  # this should raise a UniqueViolation error
    doctors[0].patients.append(patients[1])
    doctors[1].patients.append(patients[2])
    doctors[2].patients.append(patients[1])
    # or
    # doctors[0].patients = patients
    # or
    # patients[0].doctors = doctors

    db.session.commit()

##########################################################

    stmt = db.session.query(treat).filter_by(
        patient_id=patients[0].patient_id,
        doc_id=doctors[0].doc_id
    )

    # print()
    # print(stmt)
    # print(type(stmt))
    # print()
    # print(db.session.scalar(stmt), patients[0].patient_id, doctors[0].doc_id)
    # print(type(db.session.scalar(stmt)), type(
    #     patients[0].patient_id), type(doctors[0].doc_id))
    # print()

##########################################################

#     print(treat, type(treat))
#   Session.

    # seed =

    appointments = [
        Appointment(
            datetime="2000-12-12",
            place="Frog's Hollow Medical Centre",
            cost="100",
            status="Completed",
            treat_id=2  # should change this so that i'm querying treat for a particular patient and doctor combo
        ),
        Appointment(
            datetime="1999-06-13",
            place="Spring Hill Medical Centre",
            cost="206",
            status="Completed",
            treat_id=2  # should change this so that i'm querying treat for a particular patient and doctor combo
        ),
        Appointment(
            datetime="2024-10-01",
            place="UQ Medical Centre",
            cost="58",
            status="Scheduled",
            treat_id=1  # should change this so that i'm querying treat for a particular patient and doctor combo
        ),
        Appointment(
            datetime="2023-10-01",
            place="UQ Medical Centre",
            cost="77",
            status="Completed",
            treat_id=1  # should change this so that i'm querying treat for a particular patient and doctor combo
        ),
        Appointment(
            datetime="1463-09-02",
            place="London Medical Centre",
            cost="2",
            status="Completed",
            treat_id=3  # should change this so that i'm querying treat for a particular patient and doctor combo
        )
    ]

    # do i need to add and commit appointments?
    db.session.add_all(appointments)
    db.session.commit()

##########################################################

    logs = [
        Log(
            date = "2024-09-16",
            symptom = "API-induced headache",
            patient_id = 1
        ),
        Log(
            date = "1724-09-16",
            symptom = "tuberculosis",
            patient_id = 3
        ),
        Log(
            date = "1111-11-11",
            symptom = "death",
            patient_id = 2
        ),
        Log(
            date = "2023-12-3",
            symptom = "Sore spirit",
            patient_id = 2
        )
    ]
    
    db.session.add_all(logs)
    db.session.commit()

##########################################################

    # understand this (and delete?). Is this just Luis investigating querying and that the list is empty so far? AND QUERYING FOR ALL APPTS FOR A PARTICULAR PATIENT?!:
    appointments = db.session.query(Appointment).join(treat).filter(
        Appointment.treat_id == treat.c.treat_id,
        treat.c.patient_id == patients[0].patient_id
    ).all()

    # print(appointments, type(appointments))
    # print(f"len(appointments) = {len(appointments)}")
    # print()

    print("Tables seeded.")

##################################################


@app.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables droppped.")

##################################################
