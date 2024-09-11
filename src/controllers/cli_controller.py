from init import db, bcrypt
from models.patient import Patient


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
            password="password"
            is_admin=True
        ),
        Patient(
            name="Sue",
            email="sue@email.com",
            password="password",
        )
    ]
    db.session.add_all(patients)
    db.session.commit()
    print("Tables seeded.")


@app.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables droppped.")
