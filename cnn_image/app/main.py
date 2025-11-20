import io
import os
import logging
import torch
import torch.nn.functional as F
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from pythonjsonlogger import jsonlogger
from torchvision import transforms
from app.model import SimpleCNN

logger = logging.getLogger("cnn_image")
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s'))
logger.addHandler(handler)
logger.setLevel(os.getenv("LOG_LEVEL"))

app = FastAPI(title="Clasificador de Imágenes CNN")

def preprocess(img):
    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((28,28)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    return transform(img).unsqueeze(0)

CLASSES = ["0", "1", "2", "3"]

model: torch.nn.Module | None = None

@app.on_event("startup")
def load_model():
    global model
    model_path = os.getenv("CNN_MODEL_PATH")
    model = SimpleCNN(num_classes=4)
    if model_path and os.path.exists(model_path):
        try:
            model.load_state_dict(torch.load(model_path, map_location="cpu"))
            logger.info("Modelo CNN cargado", extra={"path": model_path})
        except Exception as exc:
            logger.warning("Error al cargar el modelo", extra={"error": str(exc)})
    else:
        logger.info("No se ha proporcionado un modelo preentrenado")


@app.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible.")
    content = await file.read()
    try:
        pil_img = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception as exc:
        logger.error("Imagen inválida", extra={"error": str(exc)})
        raise HTTPException(status_code=400, detail="Archivo de imagen inválido")
    tensor = preprocess(pil_img)
    model.eval()
    with torch.no_grad():
        out = model(tensor)
        probs = F.softmax(out, dim=1).squeeze().tolist()
        top_idx = int(torch.argmax(out, dim=1).item())
    limitation_note = (
        "Este clasificador es un demo y solo reconoce las 4 clases definidas."
    )
    result = {CLASSES[i]: probs[i] for i in range(len(CLASSES))}

    return {
        "clase_predecida": CLASSES[top_idx],
        "probabilidades": result,
        "nota": limitation_note
    }
