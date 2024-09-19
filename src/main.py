# ----------------------------------------------------
# app definition must come before controllers import!

# // prettier-ignore {from flask import Flask}
# // prettier-ignore {app = Flask(__name__)}

from flask import Flask 
app = Flask(__name__)
# ----------------------------------------------------

###########################################################################

import os

from init import db, ma, bcrypt, jwt
# from models.patient import Patient, patient_schema, patients_schema
# from models.models import *
from controllers.appt_controller import *
from controllers.cli_controller import *
from controllers.doctor_controller import *
from controllers.log_controller import *
from controllers.patient_controller import *
from controllers.treatment_controller import *

from marshmallow.exceptions import ValidationError


###########################################################################

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

###########################################################################

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

###########################################################################


# globally handle errors here (global = main.py) for good practice:
# generalised:
@app.errorhandler(ValidationError)
def validation_error(err):
    return {"error": err.messages}, 400


@app.errorhandler(400)
def bad_request(err):
    return {"error": err.messages}, 400


@app.errorhandler(401)
def unauthorised():
    return {"error": "You are not an authorised user."}, 401

###########################################################################

# root route
@app.route("/")
def welcome():
    """_summary_

    Returns:
        _type_: _description_
    """
    return "Welcome. Let's get healthy."

###########################################################################

# delet?:
# if __name__ == "__main__":
#     app.run(debug=True)

###########################################################################