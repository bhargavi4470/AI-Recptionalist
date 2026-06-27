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
    category = db.Column(db.String(50), nullable=False, default='appointment')

# Create the database tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

# Appointments route
@app.route('/appointments')
@app.route('/appointments.html')
def appointments():
    return render_template('appointments.html')

# Remainder route
@app.route('/remainder')
@app.route('/remainder.html')
def remainder():
    return render_template('remainder.html')

# Task route
@app.route('/task')
@app.route('/task.html')
def task():
    return render_template('task.html')



# Add appointment route
@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    data = request.json
    event_name = data['eventName']
    event_date = datetime.fromisoformat(data['eventDate'])
    email = data['email']
    category = data.get('category', 'appointment')

    # Save the appointment to the database
    new_appointment = Appointment(event_name=event_name, event_date=event_date, email=email, category=category)
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({"message": "Appointment added successfully!"}), 201

# Get events route (filtered by category if provided)
@app.route('/get_events', methods=['GET'])
def get_events():
    category = request.args.get('category')
    if category:
        events = Appointment.query.filter_by(category=category).all()
    else:
        events = Appointment.query.all()

    output = []
    for event in events:
        output.append({
            "id": event.id,
            "eventName": event.event_name,
            "eventDate": event.event_date.isoformat(),
            "email": event.email,
            "category": event.category
        })
    return jsonify(output)

# Delete event route
@app.route('/delete_event/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Appointment.query.get(id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Deleted successfully!"}), 200
    return jsonify({"error": "Event not found"}), 404

# Edit event route
@app.route('/edit_event/<int:id>', methods=['PUT'])
def edit_event(id):
    event = Appointment.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
        
    data = request.json
    event.event_name = data.get('eventName', event.event_name)
    if 'eventDate' in data:
        event.event_date = datetime.fromisoformat(data['eventDate'])
    event.email = data.get('email', event.email)
    event.category = data.get('category', event.category)
    
    db.session.commit()
    return jsonify({"message": "Updated successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)