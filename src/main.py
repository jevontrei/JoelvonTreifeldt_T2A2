# Import Flask
from flask import Flask

def create_app():
    """Application factory

    Returns:
        _type_: _description_
    """
    
    # try:
    
    # Note: app definition must come before controllers import(?)
    # Initialise app (instance of Flask class) with the current file name...?
    app = Flask(__name__)
    
    # Other imports
    from flask import jsonify
    from marshmallow.exceptions import ValidationError
    import os

    from controllers import appointments_bp, auth_bp, db_commands, doctors_bp, logs_bp, patients_bp, treatments_bp
    from init import db, ma, bcrypt, jwt
        
    # delet? do i need?
    # app.json.sort_keys = False

    # Configure database connection and JWT key using environment variables
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    
    # Initialise extensions
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(appointments_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(db_commands)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(treatments_bp)

    # Root route
    @app.route("/")
    def welcome():
        """Welcome the user

        Returns:
            _type_: _description_
        """
        # return welcome message
        return jsonify({"message": "Welcome. Let's get healthy."})

    # Globally handle generalised errors
    @app.errorhandler(ValidationError)
    def validation_error(err):
        """_summary_

        Args:
            err (_type_): _description_

        Returns:
            _type_: _description_
        """
        return jsonify(
            {"error": err.messages}
        ), 400

    @app.errorhandler(400)
    def bad_request(err):
        """_summary_

        Args:
            err (_type_): _description_

        Returns:
            _type_: _description_
        """
        return jsonify({
            "error": str(err)}
        ), 400

    @app.errorhandler(401)
    def unauthorised():
        """_summary_

        Returns:
            _type_: _description_
        """
        return jsonify(
            {"error": "Unauthorised user."}
        ), 401

    # Where exactly is this app being returned to?
    return app
