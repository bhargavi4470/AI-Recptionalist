from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(100), nullable=False)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()