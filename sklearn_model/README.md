# Servicio de Modelo Sklearn

Propósito: Proveer un pipeline de scikit-learn para una tarea de clasificación pequeña (ejemplo Iris). El entrenamiento registra métricas, parámetros y artefactos en MLflow.

Punto de acceso:
- `POST /predict` -> {"features": [f1, f2, ...]} devuelve {"prediction": [label]}
