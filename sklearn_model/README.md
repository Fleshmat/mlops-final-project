# Servicio de Modelo Sklearn

Propósito: Proveer un pipeline de scikit-learn para una tarea de clasificación pequeña (ejemplo Iris). El entrenamiento registra métricas, parámetros y artefactos en MLflow.

Entrenamiento local:

```
python -m venv .venv; .venv\Scripts\activate; pip install -r requirements.txt
python pipeline/train.py
```

Ejecutar API:

```
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

Variables de entorno:
- `MLFLOW_TRACKING_URI` por defecto `http://mlflow:5000`
- `MODEL_PATH` ruta al modelo guardado usado por la API

Punto de acceso:
- `POST /predict` -> {"features": [f1, f2, ...]} devuelve {"prediction": [label]}
