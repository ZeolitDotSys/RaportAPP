# Raport Application

Web application for generating EDAS profile report images from inspection data.

## Stack

- Backend: Python + FastAPI
- Report engine: Matplotlib + NumPy
- Frontend: HTML, CSS, Vanilla JavaScript
- User-facing UI language: Romanian
- Development/code language: English

## Project structure

```txt
backend/
  app.py
  raport_engine.py
  schemas.py
  requirements.txt
  generated/
    .gitkeep
frontend/
  index.html
  style.css
  script.js
render.yaml
.gitignore
README.md
```

## How it works

The FastAPI backend serves the frontend at `/` and exposes the report generator at `/api/generate-report`.

```txt
Public link
  -> loads Romanian frontend
  -> frontend sends form data to /api/generate-report
  -> Python creates PNG
  -> frontend shows/downloads the generated image
```

## Local backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open:

```txt
http://127.0.0.1:8000
```

Health check:

```txt
http://127.0.0.1:8000/api/health
```

## Render deployment

Use Render Web Service with the included `render.yaml` blueprint.

Manual settings if needed:

```txt
Service type: Web Service
Root Directory: backend
Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
Plan: Free
```

After deployment, Render provides a public `onrender.com` URL. Opening that URL loads the frontend and uses the Python backend from the same service.

## Next milestones

1. Add logo upload support.
2. Restore full original logo/header behavior from the desktop engine.
3. Improve generated file cleanup.
4. Add export naming options.
