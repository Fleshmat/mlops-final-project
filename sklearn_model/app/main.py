from typing import List
import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from pythonjsonlogger import jsonlogger
import pandas as pd

logger = logging.getLogger("sklearn_model")
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s'))
logger.addHandler(handler)
logger.setLevel(os.getenv("LOG_LEVEL"))

MODEL_PATH = os.getenv("MODEL_PATH")

app = FastAPI(title="Sklearn Model Service")


class Features(BaseModel):
    features: List[float]


@app.on_event("startup")
def load_model():
    global model, columns
    try:
        model, columns = joblib.load(MODEL_PATH)
        logger.info("Loaded model", extra={"path": MODEL_PATH})
    except Exception as exc:
        logger.warning("Model not loaded at startup", extra={"error": str(exc)})
        model = None


@app.post("/predict")
def predict(payload: Features):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available. Train first or set MODEL_PATH.")
    try:
        input_df = pd.DataFrame([payload.features], columns=columns)
        pred = model.predict(input_df).tolist()
        return {"prediction": pred}
    except Exception as exc:
        logger.error("Prediction failed", extra={"error": str(exc)})
        raise HTTPException(status_code=400, detail=str(exc))
