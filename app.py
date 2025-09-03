from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
RESERVATION_FILE = 'reservations.json'
CUSTOMER_FILE = 'customers.json'

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

def load_customers():
    if os.path.exists(CUSTOMER_FILE):
        with open(CUSTOMER_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

WORKOUT_FILE = 'workouts.json'

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

@app.route('/')
def index():
    workouts = load_workouts()
    reservations = load_reservations()
    customers = {c['customer_id']: c for c in load_customers()}
    for r in reservations:
        r['customer_name'] = customers.get(r['customer_id'], {}).get('name', 'Unknown')
    return render_template('index.html', workouts=workouts, reservations=reservations)

@app.route('/add', methods=['POST'])
def add_workout():
    workout = request.form.get('workout')
    duration = request.form.get('duration')
    workouts = load_workouts()
    if not workout or not duration:
        flash('Please enter both workout and duration.')
        return redirect(url_for('index'))
    try:
        duration = int(duration)
        workouts.append({'workout': workout, 'duration': duration})
        save_workouts(workouts)
        flash(f"'{workout}' added successfully!")
    except ValueError:
        flash('Duration must be a number.')
    return redirect(url_for('index'))

# Edit workout endpoint
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_workout(index):
    workouts = load_workouts()
    if index < 0 or index >= len(workouts):
        flash('Invalid workout index.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        workout = request.form.get('workout')
        duration = request.form.get('duration')
        if not workout or not duration:
            flash('Please enter both workout and duration.')
            return redirect(url_for('edit_workout', index=index))
        try:
            duration = int(duration)
            workouts[index] = {'workout': workout, 'duration': duration}
            save_workouts(workouts)
            flash('Workout updated successfully!')
            return redirect(url_for('index'))
        except ValueError:
            flash('Duration must be a number.')
            return redirect(url_for('edit_workout', index=index))
    return render_template('edit_workout.html', workout=workouts[index], index=index)

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

if __name__ == '__main__':
    app.run(debug=True)

# --- Reservation Endpoints ---

@app.route('/reservations', endpoint='reservations_list')
def reservations_list():
    reservations = load_reservations()
    customers = {c['customer_id']: c for c in load_customers()}
    for r in reservations:
        r['customer_name'] = customers.get(r['customer_id'], {}).get('name', 'Unknown')
    return render_template('reservations.html', reservations=reservations)

@app.route('/reservations/create', methods=['GET', 'POST'])
def create_reservation():
    customers = load_customers()
    if request.method == 'POST':
        machine = request.form.get('machine')
        time_slot = request.form.get('time_slot')
        customer_id = request.form.get('customer_id')
        date = request.form.get('date')
        showed_up = request.form.get('showed_up') == 'on'
        reservations = load_reservations()
        try:
            customer_id = int(customer_id)
            reservation_id = max([r['reservation_id'] for r in reservations], default=0) + 1
            reservations.append({
                'reservation_id': reservation_id,
                'machine': machine,
                'time_slot': time_slot,
                'customer_id': customer_id,
                'date': date,
                'showed_up': showed_up
            })
            save_reservations(reservations)
            flash('Reservation created successfully!')
            return redirect(url_for('reservations_list'))
        except Exception as e:
            flash('Error creating reservation: ' + str(e))
    return render_template('create_reservation.html', customers=customers)

@app.route('/reservations/edit/<int:reservation_id>', methods=['GET', 'POST'])
def edit_reservation(reservation_id):
    reservations = load_reservations()
    customers = load_customers()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if not reservation:
        flash('Reservation not found.')
        return redirect(url_for('reservations_list'))
    if request.method == 'POST':
        reservation['machine'] = request.form.get('machine')
        reservation['time_slot'] = request.form.get('time_slot')
        reservation['customer_id'] = int(request.form.get('customer_id'))
        reservation['date'] = request.form.get('date')
        reservation['showed_up'] = request.form.get('showed_up') == 'on'
        save_reservations(reservations)
        flash('Reservation updated successfully!')
        return redirect(url_for('reservations_list'))
    return render_template('edit_reservation.html', reservation=reservation, customers=customers)

@app.route('/reservations/delete/<int:reservation_id>', methods=['POST'])
def delete_reservation(reservation_id):
    reservations = load_reservations()
    idx = next((i for i, r in enumerate(reservations) if r['reservation_id'] == reservation_id), None)
    if idx is None:
        flash('Reservation not found.')
    else:
        reservations.pop(idx)
        save_reservations(reservations)
        flash('Reservation deleted.')
    return redirect(url_for('reservations_list'))

@app.route('/reservations/mark_attendance/<int:reservation_id>', methods=['POST'])
def mark_attendance(reservation_id):
    reservations = load_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if not reservation:
        flash('Reservation not found.')
    else:
        showed_up = request.form.get('showed_up') == 'on'
        reservation['showed_up'] = showed_up
        save_reservations(reservations)
        flash('Attendance updated.')
    return redirect(url_for('reservations_list'))
