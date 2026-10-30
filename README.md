# DEVOPS PULSE
## Automated CI/CD Pipeline for a Flask Web Application

DevOps Pulse is an internship project that demonstrates how a small Python web application can be tested automatically, packaged into a Docker image, and hosted online.

**Live application:** https://devops-pulse-lwon.onrender.com  
**GitHub repository:** https://github.com/sadiqfaisal/flask-cicd-demo

---

## 1. What problem does this project demonstrate?

When developers change an application, someone normally needs to check that it still works and prepare it to run. Doing these steps manually every time takes effort and can lead to mistakes.

This project automates important parts of that process:
1. A developer pushes code to GitHub.
2. GitHub Actions installs the project's Python packages.
3. Pytest runs automated checks.
4. Docker builds an image containing the application and its runtime dependencies.
5. Render separately deploys the application from the connected GitHub repository.

The workflow does not repair broken code. It reports whether the automated checks and image build succeed.

## 2. Technologies and their jobs

| Technology | What it does in this project |
|---|---|
| Python | Programming language used to write the application |
| Flask | Python framework that serves the website and API endpoints |
| HTML/CSS/JavaScript | Creates the dashboard interface and calls the API |
| Git | Tracks changes to project files |
| GitHub | Stores the source-code repository online |
| GitHub Actions | Runs the automated test and Docker build workflow |
| Pytest | Runs automated tests against the Flask application |
| Docker | Packages the application into a container image |
| Gunicorn | Runs the Flask application as a production WSGI server |
| Render | Hosts the public web application |
| PowerShell | Used for local project commands on Windows |
| VS Code | Code editor used to work on the project |

## 3. Architecture

```text
Developer edits code in VS Code
              |
              v
       Git commit and push
              |
              v
       GitHub repository
              |
              v
       GitHub Actions starts
              |
              v
       Install Python packages
              |
              v
        Run Pytest tests
              |
         Tests pass?
          /      \
        No        Yes
        |          |
     Fail job   Build Docker image
                   |
                   v
             Workflow succeeds

Separately:
GitHub repository ---> Render auto-deploy ---> Public Flask website
```

**Important:** GitHub Actions tests the code and builds the Docker image. Render's GitHub integration handles hosting and automatic deployment. The Docker image is built in the GitHub Actions runner; this workflow does not publish it to Docker Hub.

## 4. Project structure

```text
flask-cicd-demo/
├── app.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── render.yaml
├── README.md
├── tests/
│   └── test_app.py
└── .github/
    └── workflows/
        └── ci.yml
```

- `app.py`: Flask website and API routes.
- `requirements.txt`: packages needed to run the application.
- `requirements-dev.txt`: test tools used during development and CI.
- `tests/test_app.py`: automated tests.
- `Dockerfile`: instructions for building the Docker image.
- `.dockerignore`: files Docker should leave out of the image build context.
- `.gitignore`: files Git should not track.
- `.github/workflows/ci.yml`: GitHub Actions automation.
- `render.yaml`: Render service configuration.
- `README.md`: project documentation.

## 5. API endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Opens the dashboard |
| `/api/health` | Returns application health information |
| `/api/version` | Returns application version and runtime information |
| `/health` | Backwards-compatible health route |
| `/version` | Backwards-compatible version route |

Example health response:

```json
{
  "status": "healthy",
  "application": "DevOps Pulse",
  "message": "Flask application is responding"
}
```

The response also includes a timestamp.

## 6. Run locally on Windows

Open PowerShell in the project folder.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in that PowerShell window and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Install application and development dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

Run the application:

```powershell
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

Stop the local server with `Ctrl+C`.

## 7. Run automated tests

From the project folder, with the virtual environment active:

```powershell
python -m pytest -v
```

The tests check the homepage, health API, version API, and the two compatibility routes. A passing test is evidence that the tested behavior worked at the time the test ran; it does not prove that every possible behavior is error-free.

## 8. Build and run with Docker

Build the image:

```powershell
docker build -t flask-cicd-demo:latest .
```

Run a container:

```powershell
docker run --name devops-pulse-container -p 5000:5000 flask-cicd-demo:latest
```

Open `http://localhost:5000`.

In another PowerShell window, test the API:

```powershell
Invoke-RestMethod http://localhost:5000/api/health
Invoke-RestMethod http://localhost:5000/api/version
```

Stop the container with `Ctrl+C` in the window running it. Then remove the stopped container:

```powershell
docker rm devops-pulse-container
```

To see the locally built image:

```powershell
docker images
```

## 9. GitHub Actions CI workflow

The workflow file is `.github/workflows/ci.yml`.

It runs on:
- Pushes to the `main` branch.
- Pull requests targeting the `main` branch.

The job:
1. Checks out the repository.
2. Sets up Python 3.11.
3. Installs the project and test dependencies.
4. Runs Pytest.
5. Builds a Docker image tagged with the commit SHA.

If tests fail, the job stops before the Docker build. A green workflow check means the steps in that workflow completed successfully. It does not mean that GitHub Actions published an image or deployed the website.

To view a run: open the GitHub repository, select **Actions**, and open the latest workflow run.

## 10. Render deployment

Render is connected to the GitHub repository and configured to deploy from the selected branch. `render.yaml` documents the service's build command, start command, health-check path, and automatic deployment setting.

The health-check path is `/api/health`.

Live website: https://devops-pulse-lwon.onrender.com

Render's deployment is separate from the Docker image build in GitHub Actions. This project does not require Docker Hub publishing.

## 11. Security and good practices

- Never commit passwords, API keys, access tokens, or `.env` files.
- Keep dependencies in requirements files.
- Use `.gitignore` and `.dockerignore` to exclude local files and unnecessary content.
- The container runs as a non-root user.
- The GitHub Actions workflow uses read-only repository contents permission.
- Keep Python and dependencies updated, and review security advisories periodically.
- Do not put secrets directly into source code or workflow files.

## 12. Limitations

- The dashboard is an application interface with live health and version API calls. Its pipeline stage labels are explanatory; it does not read live GitHub Actions run data.
- The CI workflow builds the Docker image but does not push it to a registry.
- Render hosts the website separately through its GitHub integration.
- Automated tests cover only the behavior explicitly tested.
- Free hosting services may sleep when idle and take time to respond to the first request.

## 13. Conclusion

DevOps Pulse demonstrates a basic, practical CI/CD workflow. It combines a Flask application, automated testing, GitHub Actions, Docker image creation, and cloud hosting through Render. The project shows how developers can automate repeatable checks and package an application consistently before it is hosted online.
