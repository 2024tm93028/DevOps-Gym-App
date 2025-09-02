# DevOps-Gym-App

## ACEestFitness and Gym Flask Web Application

This is a foundational Flask web application for fitness and gym management. It allows users to log workouts and view them in a simple UI.

### Setup & Run Instructions

1. **Install Python (if not already installed)**
2. **Install Flask**
	Open PowerShell and run:
	```powershell
	pip install flask
	```
3. **Run the Application**
	In PowerShell, from the project directory, run:
	```powershell
	python app.py
	```
4. **Access the App**
	Open your browser and go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)


## Running Tests Locally

To execute the tests for this application:

1. Ensure you have `pytest` installed:
	```powershell
	pip install pytest
	```
2. Run the tests from the project directory:
	```powershell
	pytest
	```

Test results will be displayed in the terminal.

---
## GitHub Actions Pipeline Overview

This project uses GitHub Actions for CI/CD automation. The pipeline typically includes:

- **Linting & Testing:** Automatically runs tests and checks code quality on every push or pull request.
- **Build & Deploy:** Can be configured to build Docker images and deploy to cloud platforms or registries.
- **Status Badges:** Shows build/test status in pull requests and the repository.

You can find the workflow configuration in the `.github/workflows/` directory (if present).
### Features

Original desktop app code is in `ACEest_Fitness.py` (Tkinter).