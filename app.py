import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from doc_summarizer.pipeline.prediction import InferencePipeline

# Paths
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

web_app = FastAPI(
    title="Chat Text Summarization API",
    description="ML-powered summarization for conversations and long text",
    version="1.0.0",
)


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    summary: str
    input_length: int
    summary_length: int


# Mount static files (CSS, JS, assets) if folder exists
if STATIC_DIR.exists():
    web_app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@web_app.get("/")
async def root():
    """Serve the frontend app."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse({"message": "API running. Add static/index.html for UI.", "docs": "/docs"})


@web_app.get("/api/health")
async def health():
    """Health check for monitoring and UI status."""
    return {"status": "ok", "service": "chat-summarization"}


@web_app.get("/api/metrics")
async def get_metrics():
    """Return model evaluation metrics (ROUGE) if available."""
    metrics_path = BASE_DIR / "artifacts" / "model_evaluation" / "metrics.csv"
    if not metrics_path.exists():
        return JSONResponse({"available": False, "message": "Metrics not yet computed."})
    try:
        import csv
        with open(metrics_path) as f:
            reader = csv.DictReader(f)
            row = next(reader, None)
        if not row:
            return {"available": False}
        return {"available": True, "metrics": {k: float(v) for k, v in row.items()}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@web_app.post("/api/predict", response_model=PredictResponse)
async def predict(payload: PredictRequest):
    """Summarize input text (e.g. chat or long dialogue)."""
    text = (payload.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    try:
        runner = InferencePipeline()
        summary = runner.run_prediction(text)
        return PredictResponse(
            summary=summary,
            input_length=len(text.split()),
            summary_length=len(summary.split()),
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@web_app.get("/api/train")
async def run_training():
    """Trigger training pipeline (long-running). For UI status only."""
    try:
        os.system("python main.py")
        return {"status": "completed", "message": "Training finished."}
    except Exception as err:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(err)})


# Legacy route for backward compatibility
@web_app.post("/predict")
async def predict_legacy(input_text: str = ""):
    try:
        runner = InferencePipeline()
        result = runner.run_prediction(input_text or "")
        return result
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


if __name__ == "__main__":
    uvicorn.run(web_app, host="0.0.0.0", port=8191)
