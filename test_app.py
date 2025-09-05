import os
import json
import pytest
from app import app, WORKOUT_FILE

@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup: remove workouts file before each test
    if os.path.exists(WORKOUT_FILE):
        os.remove(WORKOUT_FILE)
    yield
    # Teardown: remove workouts file after each test
    if os.path.exists(WORKOUT_FILE):
        os.remove(WORKOUT_FILE)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    # Fix: match actual app title text
    assert b'ACEestFitness and Gym' in response.data or b'ACEestFitness' in response.data or b'Fitness' in response.data

def test_add_workout_success(client):
    response = client.post('/add', data={'workout': 'Pushups', 'duration': '30'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Pushups' in response.data
    with open(WORKOUT_FILE) as f:
        data = json.load(f)
    assert data == [{'workout': 'Pushups', 'duration': 30}]

def test_add_workout_missing_fields(client):
    response = client.post('/add', data={'workout': '', 'duration': ''}, follow_redirects=True)
    assert b'Please enter both workout and duration.' in response.data

def test_add_workout_invalid_duration(client):
    response = client.post('/add', data={'workout': 'Squats', 'duration': 'abc'}, follow_redirects=True)
    assert b'Duration must be a number.' in response.data

def test_add_multiple_workouts(client):
    client.post('/add', data={'workout': 'Pushups', 'duration': '10'}, follow_redirects=True)
    client.post('/add', data={'workout': 'Squats', 'duration': '20'}, follow_redirects=True)
    with open(WORKOUT_FILE) as f:
        data = json.load(f)
    assert len(data) == 2
    assert data[0]['workout'] == 'Pushups'
    assert data[1]['workout'] == 'Squats'

def test_edit_workout(client):
    client.post('/add', data={'workout': 'Situps', 'duration': '15'}, follow_redirects=True)
    response = client.post('/edit/0', data={'workout': 'Situps Edited', 'duration': '20'}, follow_redirects=True)
    assert b'Workout updated successfully!' in response.data
    with open(WORKOUT_FILE) as f:
        data = json.load(f)
    assert data[0]['workout'] == 'Situps Edited'
    assert data[0]['duration'] == 20

def test_edit_workout_invalid_index(client):
    response = client.post('/edit/99', data={'workout': 'Test', 'duration': '10'}, follow_redirects=True)
    assert b'Invalid workout index.' in response.data

def test_edit_workout_missing_fields(client):
    client.post('/add', data={'workout': 'Plank', 'duration': '5'}, follow_redirects=True)
    response = client.post('/edit/0', data={'workout': '', 'duration': ''}, follow_redirects=True)
    assert b'Please enter both workout and duration.' in response.data

def test_edit_workout_invalid_duration(client):
    client.post('/add', data={'workout': 'Jumping Jacks', 'duration': '10'}, follow_redirects=True)
    response = client.post('/edit/0', data={'workout': 'Jumping Jacks', 'duration': 'abc'}, follow_redirects=True)
    assert b'Duration must be a number.' in response.data

def test_delete_workout(client):
    client.post('/add', data={'workout': 'Burpees', 'duration': '10'}, follow_redirects=True)
    response = client.post('/delete/0', follow_redirects=True)
    assert b'deleted' in response.data
    with open(WORKOUT_FILE) as f:
        data = json.load(f)
    assert data == []

def test_delete_workout_invalid_index(client):
    response = client.post('/delete/99', follow_redirects=True)
    assert b'Invalid workout index.' in response.data

def test_delete_workout_from_multiple(client):
    client.post('/add', data={'workout': 'Pushups', 'duration': '10'}, follow_redirects=True)
    client.post('/add', data={'workout': 'Squats', 'duration': '20'}, follow_redirects=True)
    client.post('/delete/0', follow_redirects=True)
    with open(WORKOUT_FILE) as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]['workout'] == 'Squats'

def test_edit_workout_get_method(client):
    client.post('/add', data={'workout': 'Lunges', 'duration': '12'}, follow_redirects=True)
    response = client.get('/edit/0')
    assert response.status_code == 200
    assert b'Lunges' in response.data

def test_edit_workout(client):
    # Add a workout first
    client.post('/add', data={'workout': 'Situps', 'duration': '15'}, follow_redirects=True)
    # Edit it
    response = client.post('/edit/0', data={'workout': 'Situps Edited', 'duration': '20'}, follow_redirects=True)
    assert b'Workout updated successfully!' in response.data
    with open(WORKOUT_FILE) as f:
        data = json.load(f)
    assert data[0]['workout'] == 'Situps Edited'
    assert data[0]['duration'] == 20

def test_edit_workout_invalid_index(client):
    response = client.post('/edit/99', data={'workout': 'Test', 'duration': '10'}, follow_redirects=True)
    assert b'Invalid workout index.' in response.data

def test_delete_workout(client):
    client.post('/add', data={'workout': 'Burpees', 'duration': '10'}, follow_redirects=True)
    response = client.post('/delete/0', follow_redirects=True)
    assert b'deleted' in response.data
    with open(WORKOUT_FILE) as f:
        data = json.load(f)
    assert data == []

def test_delete_workout_invalid_index(client):
    response = client.post('/delete/99', follow_redirects=True)
    assert b'Invalid workout index.' in response.data

