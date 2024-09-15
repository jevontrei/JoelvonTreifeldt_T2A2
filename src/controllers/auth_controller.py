from init import db
from main import app
from models.models import treat

@app.route("/treat/")
def get_all_treatments():
    stmt = db.select(treat)
    treatments = db.session.scalars(stmt)
    return db.session.dump(treatments)
    # SCHEMA? define one?!