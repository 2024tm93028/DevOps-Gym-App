SESSION_FILE = 'sessions.json'

def load_sessions():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_sessions(sessions):
    with open(SESSION_FILE, 'w') as f:
        json.dump(sessions, f)

@app.route('/sessions')
def sessions():
    sessions = load_sessions()
    return render_template('sessions.html', sessions=sessions)

@app.route('/add_session', methods=['POST'])
def add_session():
    name = request.form.get('name')
    date = request.form.get('date')
    time = request.form.get('time')
    sessions = load_sessions()
    if not name or not date or not time:
        flash('Please enter all session details.')
        return redirect(url_for('sessions'))
    sessions.append({'name': name, 'date': date, 'time': time})
    save_sessions(sessions)
    flash('Session reserved successfully!')
    return redirect(url_for('sessions'))
from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

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
    return render_template('index.html', workouts=workouts)

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
    return render_template('edit.html', workout=workouts[index], index=index)

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

from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

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
    return render_template('index.html', workouts=workouts)

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

if __name__ == '__main__':
    app.run(debug=True)
