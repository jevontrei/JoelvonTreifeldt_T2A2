from flask import Flask
from init import db, ma, bcrypt, jwt
from models.patient import Patient, patient_schema, patients_schema
# from controllers.patient_controller import welcome
# from controllers.cli_controller import welcome

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://joelvontreifeldt:password@localhost:5432/medical"
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

app.config["JWT_SECRET_KEY"] = "secret"
# app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)


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


@app.route("/")
def welcome():
    return "Welcome. Let's get healthy."


@app.route("/patients/")
def get_all_patients():
    stmt = db.select(Patient).order_by(Patient.name)
    patients = db.session.scalars(stmt)
    return patients_schema.dump(patients)


# delet this?:
# if __name__ == "__main__":
#     app.run(debug=True)
