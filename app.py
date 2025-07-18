from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define a model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(100), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Appointments route
@app.route('/appointments')
def appointments():
    return render_template('appointments.html')



# Add appointment route
@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    data = request.json
    event_name = data['eventName']
    event_date = datetime.fromisoformat(data['eventDate'])
    email = data['email']

    # Save the appointment to the database
    new_appointment = Appointment(event_name=event_name, event_date=event_date, email=email)
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({"message": "Appointment added successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)