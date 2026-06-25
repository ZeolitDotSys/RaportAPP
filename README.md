#Raport Application

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
.gitignore
README.md
```

## Local backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Backend URL:

```txt
http://127.0.0.1:8000
```

Health check:

```txt
http://127.0.0.1:8000/api/health
```

## Local frontend setup

Open `frontend/index.html` in the browser.

During local development, `frontend/script.js` points to:

```js
const API_BASE_URL = "http://127.0.0.1:8000";
```

This can be changed later for deployment.

## Next milestones

1. Add the cleaned report engine from the original desktop Python app.
2. Add logo upload support.
3. Improve generated file cleanup.
4. Prepare Render/Railway deployment.
