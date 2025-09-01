
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
