# figure out privacy settings.

# somehow authorise doctors to view logs, but not all logs. you may not want your dentist viewing your psychology details.

# in case of emergency/hospital/ambulance etc, there should be some contingency access for health professionals like paramedics, surgeons, ER doctors/nurses, etc

###########################################################################

from flask import Blueprint, request

###########################################################################

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

###########################################################################

@auth_bp.route("/register/<str:patient or doctor?>", methods=["POST"])
def register_user(user):
    # try:
    
    # fetch data, deserialise it, store in variable
    body_data = request.get_json()
    
    if user == "patient":
        
        # remember to validate input!
        # define new instance of Patient class
        patient = Patient(
            name=body_data.get("name"),
            email=body_data.get("email"),
            password=body_data.get("password"),
            dob=body_data.get("dob"),
            sex=body_data.get("sex"),
            is_admin=body_data.get("is_admin"),
        )
        
        # hash password

        db.session.add(patient)
        db.session.commit()

        return patient_schema.dump(patient), 201
        
    elif user == "doctor":
        doctor = Doctor(
            name=body_data.get("name"),
            email=body_data.get("email"),
            password=body_data.get("password")
        )
        
        # hash password

        db.session.add(doctor)
        db.session.commit()

        return doctor_schema.dump(doctor), 201
    
    else:
        return jsonify({"message": f"User type {user} not valid. User type must be 'patient' or 'doctor'."})#, 400?
    
    # except ?:
    

###########################################################################

# @auth_bp.route("/login", methods=["POST"])
# def login_user():
#     body_data = request.get_json()
    
#     stmt = db.select(User).filter_by(email=body_data["email"])
    
#     user = db.session.scalar(stmt)
    
#     if user and bcrypt.check_password_hash(user.password, body_data.get("password")):

#         token = create_access_token(
#             identity=str(user.id),
#             expires_delta=timedelta(days=1)
#         )
        
#         return {"email": user.email, "is_admin": user.is_admin, "token": token}
    
#     else:
#         return {"error": "Invalid email or password"}, 400

###########################################################################
