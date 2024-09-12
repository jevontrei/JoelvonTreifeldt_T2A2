from init import db, bcrypt
from models.patient import Patient
from models.doctor import Doctor
from main import app


@app.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created.")


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
    
    db.session.commit()
    
    print("Tables seeded.")


@app.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables droppped.")
