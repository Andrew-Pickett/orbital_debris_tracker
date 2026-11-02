# Orbital Debris Tracker

A web app for exploring and visualising orbital debris and satellite data.

## Running locally

From the project directory, activate the virtual environment and install the dependencies:

```bash
source .venv/bin/activate
uv add -r requirements.txt
uv run uvicorn app.main:app --reload
```

Visit http://127.0.0.1:8000/health to check the app, or http://127.0.0.1:8000/docs to explore its API.

Run the tests in a terminal:

```bash
python -m pytest
```