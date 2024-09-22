# import Flask
from flask import Flask

# application factory
def create_app():
    # try:
    
    # note: app definition must come before controllers import(?)
    # initialise app (instance of Flask class) with the current file name...?
    app = Flask(__name__)
    
    # other imports
    from flask import jsonify
    from marshmallow.exceptions import ValidationError
    import os

    from controllers import appointments_bp, auth_bp, db_commands, doctors_bp, logs_bp, patients_bp, treatments_bp
    from init import db, ma, bcrypt, jwt
        
    # do i need this?
    # app.json.sort_keys = False

    # configuration on database connection and JWT key
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    
    # initialise extensions
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

    # globally handle generalised errors
    @app.errorhandler(ValidationError)
    def validation_error(err):
        """"""
        return jsonify({"error": err.messages}), 400

    # i'm getting Insomnia error "AttributeError: 'BadRequest' object has no attribute 'message' etc"?!
    @app.errorhandler(400)
    def bad_request(err):
        # this is giving me issues. change it?!
        return jsonify({"error": err.messages}), 400

    @app.errorhandler(401)
    def unauthorised():
        return jsonify({"error": "Unauthorised user."}), 401

    # root route
    @app.route("/")
    def welcome():
        """Welcome the user

        Returns:
            _type_: _description_
        """
        # return welcome message
        return jsonify({"message": "Welcome. Let's get healthy."})

    return app

    # except Exception as e:
    #         return jsonify(
    #             {
    #                 "error": "...?"
    #             }
    #         ), 400  # ?