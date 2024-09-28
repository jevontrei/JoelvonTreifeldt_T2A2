# Import Flask
from flask import Flask


def create_app():
    """Application factory; create the Flask app.

    Returns:
        Flask app object.
    """

    # Initialise app (instance of Flask class) before imports
    app = Flask(__name__)

    # Other imports
    from flask import jsonify
    from marshmallow.exceptions import ValidationError
    import os

    from controllers import appointments_bp, auth_bp, db_commands, doctors_bp, logs_bp, patients_bp, treatments_bp
    from init import db, ma, bcrypt, jwt

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

##################################################################

    # http://localhost:5000/

    # Root route
    @app.route("/")
    def welcome():
        """Welcome the user.

        Returns:
            JSON: Welcome message.
        """
        return jsonify(
            {"message": "Welcome. Let's get healthy."}
        )

##################################################################

    # Globally handle generalised errors
    
    @app.errorhandler(ValidationError)
    def validation_error(e):
        """_summary_

        Args:
            e: Error.

        Returns:
            tuple: Error message (JSON) and a HTTP response status code.
        """
        return jsonify({"error": e.messages}), 400

    @app.errorhandler(400)
    def bad_request(e):
        """_summary_

        Args:
            e: Error.

        Returns:
            tuple: Error message (JSON) and a HTTP response status code.
        """
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(401)
    def unauthorised(e):
        """_summary_

        Args:
            e: Error.
            
        Returns:
            tuple: Error message (JSON) and a HTTP response status code.
        """
        return jsonify({"error": "Unauthorised user."}), 401

    @app.errorhandler(404)
    def not_found(e):
        """In case an invalid endpoint is requested.

        Args:
            e: Error.
            
        Returns:
            tuple: Error message (JSON) and HTTP response status code
        """
        return jsonify({"error": "Route does not exist."}), 404

    # Return app to WSGI server
    return app
