from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from raport_engine import create_report
from schemas import ReportRequest, ReportResponse

BASE_DIR = Path(__file__).resolve().parent
GENERATED_DIR = BASE_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="EDAS Raport API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/generated", StaticFiles(directory=GENERATED_DIR), name="generated")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/generate-report", response_model=ReportResponse)
def generate_report(payload: ReportRequest):
    filename = f"report_{uuid4().hex}.png"
    output_path = GENERATED_DIR / filename

    metadata = create_report(payload.model_dump(), output_path)

    return ReportResponse(
        image_url=f"/generated/{filename}",
        filename=filename,
        distance=metadata["distance"],
        level_difference=metadata["level_difference"],
        start_manhole=metadata["start_manhole"],
        end_manhole=metadata["end_manhole"],
    )
