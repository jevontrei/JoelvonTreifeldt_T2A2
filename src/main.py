# ----------------------------------------------------
# app definition must come before controllers import!

# // prettier-ignore {from flask import Flask}
# // prettier-ignore {app = Flask(__name__)}

from flask import Flask 
app = Flask(__name__)
# ----------------------------------------------------

import os

from init import db, ma, bcrypt, jwt
# from models.patient import Patient, patient_schema, patients_schema
# from models.models import *
from controllers.appt_controller import *
from controllers.cli_controller import *
from controllers.doctor_controller import *
from controllers.log_controller import *
from controllers.patient_controller import *
from controllers.treat_controller import *


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)


@app.route("/")
def welcome():
    return "Welcome. Let's get healthy."


# if __name__ == "__main__":
#     app.run(debug=True)
