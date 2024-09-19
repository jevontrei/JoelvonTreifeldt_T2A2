from init import db
from models.models import Treatment, treatment_schema, treatments_schema
from main import app
from flask import jsonify

# THESE ALL NEED TO CHANGE BC I AM NOW USING DB.MODEL FOR Treatment. THEY NEED TO BE SERIALISED NOW!

#####################################################

@app.route("/treatments/")
def get_all_treatments():
    # create SQL statement
    # SELECT * FROM treatment;
    stmt = db.select(Treatment)
    # execute statement, store in an iterable object
    treatments = db.session.scalars(stmt)
    # serialise object to JSON, return it
    return treatments_schema.dump(treatments)


#####################################################

@app.route("/treatments/<int:treatment_id>")
def get_a_treatmeant(treatment_id):
    # SELECT * FROM treatment WHERE treatment_id=treatment_id ... ?;
    stmt = db.select(Treatment).filter_by(treatment_id=treatment_id)
    treatment = db.session.scalar(stmt)
    return treatment_schema.dump(treatment)

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
