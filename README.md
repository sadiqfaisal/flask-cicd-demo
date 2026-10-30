# Automated Web Application Build and Deployment Using CI/CD

## 1. Project Overview

This project demonstrates how a web application can be automatically
tested, packaged and prepared for deployment using DevOps tools.

The application is developed using Python and Flask.

GitHub Actions automates the build and testing process whenever
code is pushed to the main branch.

## 2. Problem Statement

Manual application testing and deployment require repetitive work.
They can also introduce human errors.

This project demonstrates automation of application testing,
Docker image creation and optional image publishing and deployment.

## 3. Objectives

- Develop a Flask web application.
- Maintain source code using Git and GitHub.
- Automate application testing.
- Build a Docker image.
- Optionally publish the image to Docker Hub.
- Optionally trigger deployment to Render.

## 4. Technologies Used

- Python: Application programming.
- Flask: Web framework.
- Pytest: Automated testing.
- Git: Version control.
- GitHub: Source code repository.
- GitHub Actions: CI/CD automation.
- Docker: Application containerization.
- Docker Hub: Container image registry.
- Render: Optional cloud deployment platform.

## 5. Project Architecture

Developer
   |
   v
GitHub Repository
   |
   v
GitHub Actions Workflow
   |
   v
Install Dependencies
   |
   v
Run Automated Tests
   |
   v
Build Docker Image
   |
   v
Optional Docker Hub Publishing
   |
   v
Optional Render Deployment

## 6. Project Structure

flask-cicd-demo/
|
|-- app.py
|-- requirements.txt
|-- Dockerfile
|-- .dockerignore
|-- README.md
|-- tests/
|   |-- test_app.py
|
|-- .github/
    |-- workflows/
        |-- ci.yml

## 7. Local Execution

Create virtual environment:

python -m venv .venv

Activate it in Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py

Open browser:

http://127.0.0.1:5000

Health check:

http://127.0.0.1:5000/health

Version:

http://127.0.0.1:5000/version

## 8. Automated Testing

Execute:

python -m pytest -v

Three tests verify:
- Homepage availability.
- Application health.
- Application version.

## 9. CI/CD Execution

1. Push source code to GitHub.
2. GitHub Actions detects the push.
3. The workflow downloads the source code.
4. Python dependencies are installed.
5. Automated tests are executed.
6. A Docker image is built.
7. If Docker Hub credentials are configured, the image is published.
8. If a Render deploy hook is configured, deployment is triggered.

## 10. Expected Result

All three automated tests should pass.

The Docker image should build successfully on the GitHub runner.

Optional publishing and cloud deployment require their respective credentials.

## 11. Conclusion

This project demonstrates a basic CI/CD workflow by
automating application testing and container image building.

It reduces repetitive manual work and demonstrates
important DevOps concepts such as automation,
version control, testing and containerization.
