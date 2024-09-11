from flask import Flask
from init import db, ma, bcrypt, jwt

# put this in terminal to save having to cd into src every time?:
# export FLASK_APP=src/<your_application_file_name>.py


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://joelvontreifeldt:123456@localhost:5432/trello_db"
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

app.config["JWT_SECRET_KEY"] = "secret"
# app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

# db.init_app(app)
# ma.init_app(app)
# bcrypt.init_app(app)
# jwt.init_app(app)
