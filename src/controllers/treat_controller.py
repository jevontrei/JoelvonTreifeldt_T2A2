from init import db
from models.models import Treat
from main import app
from flask import jsonify

#####################################################


# THESE ALL NEED TO CHANGE BC I AM NOW USING DB.MODEL FOR TREAT. THEY NEED TO BE SERIALISED NOW!

@app.route("/treatments/")
def get_all_treatments():
    # SELECT * FROM treat;
    stmt = db.select(treat)
    with db.session.begin():
        results = db.session.execute(stmt).fetchall()
    treats = [row._asdict() for row in results]
    return jsonify(treats)


#####################################################

@app.route("/treatments/<int:treat_id>")
def get_a_treatmeant(treat_id):
    ...

#####################################################

# @app.route("/treatments/patients/<patient_id>")
# def get_patient_treatments():

#####################################################


# @app.route("/treatments/doctors/<doc_id>")
# def get_doctor_treatments():

#####################################################


# @app.route("/treatments/doctors/<doc_id>")
# def get_doctor_patients?():

#####################################################


# @app.route("/treatments/", methods=["PUT", "PATCH"])
# def

#####################################################


# @app.route("/treatments/", methods=["DELETE"])
# def


#####################################################
