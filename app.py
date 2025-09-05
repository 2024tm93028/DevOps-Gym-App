
from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os


app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

WORKOUT_FILE = 'workouts.json'
RESERVATION_FILE = 'reservations.json'
CUSTOMER_FILE = 'customers.json'

def load_customers():
    if os.path.exists(CUSTOMER_FILE):
        with open(CUSTOMER_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_customers(customers):
    with open(CUSTOMER_FILE, 'w') as f:
        json.dump(customers, f)
def load_reservations():
    if os.path.exists(RESERVATION_FILE):
        with open(RESERVATION_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_reservations(reservations):
    with open(RESERVATION_FILE, 'w') as f:
        json.dump(reservations, f)

def load_workouts():
    if os.path.exists(WORKOUT_FILE):
        with open(WORKOUT_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_workouts(workouts):
    with open(WORKOUT_FILE, 'w') as f:
        json.dump(workouts, f)


# Landing page
@app.route('/')
def landing():
    return render_template('landing.html')

# Workouts page
@app.route('/workouts')
def index():
    workouts = load_workouts()
    customers = load_customers()
    return render_template('index.html', workouts=workouts, customers=customers)

@app.route('/add', methods=['POST'])
def add_workout():
    workout = request.form.get('workout')
    duration = request.form.get('duration')
    customer_id = request.form.get('customer_id')
    workouts = load_workouts()
    customers = load_customers()
    if not workout or not duration or not customer_id:
        flash('Please enter workout, duration, and select a customer.')
        return redirect(url_for('index'))
    try:
        duration = int(duration)
        customer_id = int(customer_id)
        customer = next((c for c in customers if c['id'] == customer_id), None)
        if not customer:
            flash('Selected customer does not exist.')
            return redirect(url_for('index'))
        workouts.append({'workout': workout, 'duration': duration, 'customer_id': customer_id})
        save_workouts(workouts)
        flash(f"'{workout}' added for {customer['name']} successfully!")
    except ValueError:
        flash('Duration and customer must be valid.')
    return redirect(url_for('index'))

# Edit workout endpoint
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_workout(index):
    workouts = load_workouts()
    customers = load_customers()
    if index < 0 or index >= len(workouts):
        flash('Invalid workout index.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        workout = request.form.get('workout')
        duration = request.form.get('duration')
        customer_id = request.form.get('customer_id')
        if not workout or not duration or not customer_id:
            flash('Please enter workout, duration, and select a customer.')
            return redirect(url_for('edit_workout', index=index))
        try:
            duration = int(duration)
            customer_id = int(customer_id)
            customer = next((c for c in customers if c['id'] == customer_id), None)
            if not customer:
                flash('Selected customer does not exist.')
                return redirect(url_for('edit_workout', index=index))
            workouts[index] = {'workout': workout, 'duration': duration, 'customer_id': customer_id}
            save_workouts(workouts)
            flash('Workout updated successfully!')
            return redirect(url_for('index'))
        except ValueError:
            flash('Duration and customer must be valid.')
            return redirect(url_for('edit_workout', index=index))
    return render_template('edit_workouts.html', workout=workouts[index], index=index, customers=customers)

# Delete workout endpoint
@app.route('/delete/<int:index>', methods=['POST'])
def delete_workout(index):
    workouts = load_workouts()
    if index < 0 or index >= len(workouts):
        flash('Invalid workout index.')
    else:
        removed = workouts.pop(index)
        save_workouts(workouts)
        flash(f"Workout '{removed['workout']}' deleted.")
    return redirect(url_for('index'))

# Add endpoints to manage customer reservations such as customer name, contact information, reservation date and time, and machine type.


@app.route('/reservations')
def reservations():
    reservations = load_reservations()
    customers = load_customers()
    return render_template('reservations.html', reservations=reservations, customers=customers)

# Mark attendance
@app.route('/mark_attendance/<int:reservation_id>', methods=['POST'])
def mark_attendance(reservation_id):
    reservations = load_reservations()
    if 0 <= reservation_id < len(reservations):
        reservations[reservation_id]['attendance'] = 'Present'
        save_reservations(reservations)
        flash('Attendance marked as Present.')
    else:
        flash('Invalid reservation.')
    return redirect(url_for('reservations'))

# Mark no-show
@app.route('/mark_noshow/<int:reservation_id>', methods=['POST'])
def mark_noshow(reservation_id):
    reservations = load_reservations()
    if 0 <= reservation_id < len(reservations):
        reservations[reservation_id]['attendance'] = 'No-Show'
        save_reservations(reservations)
        flash('Attendance marked as No-Show.')
    else:
        flash('Invalid reservation.')
    return redirect(url_for('reservations'))

@app.route('/create_reservation', methods=['GET', 'POST'])
def create_reservation():
    customers = load_customers()
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        date = request.form.get('date')
        time = request.form.get('time')
        machine_type = request.form.get('machine_type')
        reservations = load_reservations()
        if not customer_id or not date or not time or not machine_type:
            flash('Please fill all fields.')
            return render_template('create_reservation.html', customers=customers)
        try:
            customer_id = int(customer_id)
            customer = next((c for c in customers if c['id'] == customer_id), None)
            if not customer:
                flash('Selected customer does not exist.')
                return render_template('create_reservation.html', customers=customers)
            reservations.append({
                'customer_id': customer_id,
                'date': date,
                'time': time,
                'machine_type': machine_type
            })
            save_reservations(reservations)
            flash('Reservation created successfully!')
            return redirect(url_for('reservations'))
        except ValueError:
            flash('Invalid customer.')
            return render_template('create_reservation.html', customers=customers)
    return render_template('create_reservation.html', customers=customers)

@app.route('/edit_reservation/<int:reservation_id>', methods=['GET', 'POST'])
def edit_reservation(reservation_id):
    if request.method == 'POST':
        # Handle reservation editing
        return redirect(url_for('reservations'))
    return render_template('edit_reservation.html', reservation=load_reservation(reservation_id))

@app.route('/delete_reservation/<int:reservation_id>', methods=['POST'])
def delete_reservation(reservation_id):
    # Handle reservation deletion
    return redirect(url_for('reservations'))

# ...existing code...

# Customer management routes (must be after app = Flask(__name__) and all helpers)
from copy import deepcopy

@app.route('/customers')
def customers():
    customers = load_customers()
    return render_template('customers.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    customers = load_customers()
    name = request.form.get('name')
    contact = request.form.get('contact')
    email = request.form.get('email')
    if not name or not contact or not email:
        flash('Please fill all fields.')
        return redirect(url_for('customers'))
    # Generate new id
    new_id = max([c['id'] for c in customers], default=0) + 1
    customers.append({'id': new_id, 'name': name, 'contact': contact, 'email': email})
    save_customers(customers)
    flash('Customer added successfully!')
    return redirect(url_for('customers'))

@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customers = load_customers()
    customer = next((c for c in customers if c['id'] == customer_id), None)
    if not customer:
        flash('Customer not found.')
        return redirect(url_for('customers'))
    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form.get('contact')
        email = request.form.get('email')
        if not name or not contact or not email:
            flash('Please fill all fields.')
            return render_template('edit_customer.html', customer=customer)
        customer['name'] = name
        customer['contact'] = contact
        customer['email'] = email
        save_customers(customers)
        flash('Customer updated successfully!')
        return redirect(url_for('customers'))
    return render_template('edit_customer.html', customer=deepcopy(customer))

@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customers = load_customers()
    new_customers = [c for c in customers if c['id'] != customer_id]
    if len(new_customers) == len(customers):
        flash('Customer not found.')
    else:
        save_customers(new_customers)
        flash('Customer deleted successfully!')
    return redirect(url_for('customers'))

if __name__ == '__main__':
    app.run(debug=True)
