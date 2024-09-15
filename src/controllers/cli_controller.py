from init import db, bcrypt
from models.models import Patient, Doctor, auth, Appointment
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
            name="Sue",
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
            name="John Smith",
            email="john@email.com",
            password="password",
        )
    ]

    db.session.add_all(doctors)
    # db.session.add_all([patients, doctors])
    doctors[0].patients.append(patients[1])
    doctors[0].patients.append(patients[0])
    doctors[1].patients.append(patients[1])
    # or
    # doctors[0].patients = patients
    # or
    # patients[0].doctors = doctors

    db.session.commit()

    stmt = db.session.query(auth).filter_by(
        patient_id=patients[0].patient_id,
        doc_id=doctors[0].doc_id
    )

    print()
    print(stmt)
    print(type(stmt))
    print()
    print(db.session.scalar(stmt), patients[0].patient_id, doctors[0].doc_id)
    print(type(db.session.scalar(stmt)), type(
        patients[0].patient_id), type(doctors[0].doc_id))
    print()

##########################################################

#     print(auth, type(auth))
#   Session.

    # seed = 

    appointments = [
        Appointment(
            datetime="2000-12-12",
            place="Frog's Hollow Medical Centre",
            cost="100",
            status="Completed",
            auth_id=2  # should change this so that i'm querying auth for a particular patient and doctor combo
        ),
        Appointment(
            datetime="2024-10-1",
            place="UQ Medical Centre",
            cost="58",
            status="Scheduled",
            auth_id=1  # should change this so that i'm querying auth for a particular patient and doctor combo
        )
    ]

    # with db.engine.connect() as connection:
    #     connection.execute(insert(a))

    # do i need to add and commit appointments?
    db.session.add_all(appointments)
    db.session.commit()

##########################################################

    # understand this (and delete?). Is this just Luis investigating querying and that the list is empty so far?:
    appointments = db.session.query(Appointment).join(auth).filter(
        Appointment.auth_id == auth.c.auth_id,
        auth.c.patient_id == patients[0].patient_id
    ).all()

    print(appointments, type(appointments))
    print(f"len(appointments) = {len(appointments)}")
    print()

    print("Tables seeded.")

##################################################


@app.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables droppped.")

##################################################
