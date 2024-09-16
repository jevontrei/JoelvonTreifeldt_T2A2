from init import db
from models.models import treat
from main import app
from flask import jsonify

@app.route("/treatments/")
def get_all_treatments():
    
    stmt = db.select(treat)
    # print()
    # print(f"stmt = {stmt}")
    
    with db.session.begin():
        results = db.session.execute(stmt).fetchall()
    # print(results[0])

    treats = [row._asdict() for row in results]
    
    # treatments = db.session.scalars(stmt)
    # print(f"treatments = {treatments}")
    # print()
    
    # return db.session.dump(treatments)
    
    return jsonify(treats)

    # SCHEMA!? define one?!
    
    
#####################################################
    
@app.route("/treatments/<int:treat_id>")
def get_a_treat(treat_id):
    ...
    
#####################################################
    
# @app.route("/treatments/patients/<patient_id>")
# def get_patient_treatments():
    
# @app.route("/treatments/doctors/<doc_id>")
# def get_doctor_treatments():
    
# @app.route("/treatments/", methods=["PUT", "PATCH"])
# def

# @app.route("/treatments/", methods=["DELETE"])
# def
