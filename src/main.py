from flask import Flask

# application factory
def create_app():
    # app definition must come before controllers import
    # initialise? app / instance of Flask class with the current file name...?
    app = Flask(__name__)
    
    # imports
    from flask import jsonify
    from marshmallow.exceptions import ValidationError
    import os

    from init import db, ma, bcrypt, jwt

    from controllers.appt_controller import appointments_bp
    from controllers.auth_controller import auth_bp
    from controllers.cli_controller import db_commands
    from controllers.doctor_controller import doctors_bp
    from controllers.log_controller import logs_bp
    from controllers.patient_controller import patients_bp
    from controllers.treatment_controller import treatments_bp
        
    # app.json.sort_keys = False

    # configuration on database connection and ?
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    
    # initialise ...?
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # register blueprints
    app.register_blueprint(appointments_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(db_commands)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(treatments_bp)

    # globally handle errors here (global = main.py) for good practice:
    # generalised:
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return jsonify({"error": err.messages}), 400

    # i'm getting Insomnia error "AttributeError: 'BadRequest' object has no attribute 'message' etc"
    @app.errorhandler(400)
    def bad_request(err):
        # this is giving me issues. change it
        return jsonify({"error": err.messages}), 400

    @app.errorhandler(401)
    def unauthorised():
        return jsonify({"error": "Unauthorised user."}), 401

    # root route
    @app.route("/")
    def welcome():
        """_summary_

        Returns:
            _type_: _description_
        """
        # return ...?
        return jsonify({"message": "Welcome. Let's get healthy."})

    return app
