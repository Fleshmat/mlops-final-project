from typing import Any, Dict, List, Optional
import os
import logging
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("llm_connector")
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s'))
logger.addHandler(handler)
logger.setLevel(os.getenv("LOG_LEVEL"))

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

app = FastAPI(title="LLM Connector")



class Query(BaseModel):
    question: str
    history: Optional[List[Dict[str, str]]] = None


@app.post("/query")
def query_llm(payload: Query) -> Any:
    logger.info("Received query", extra={"question": payload.question})
    try:
        body = {"model": OLLAMA_MODEL, "prompt": payload.question, "stream": False,"history": payload.history or []}
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json=body, timeout=70)
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("response")
        logger.info("Ollama response", extra={"status": resp.status_code})
        return {"answer": answer}
    except Exception as exc:
        logger.error("Error contacting Ollama", extra={"error": str(exc)})
        raise HTTPException(status_code=503, detail="LLM backend unreachable")
