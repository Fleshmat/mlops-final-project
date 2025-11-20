# Proyecto Final MLOps (Estructura)

Este repositorio contiene cuatro servicios:

- `llm_connector`: Servicio FastAPI que reenvía consultas a Ollama (por defecto `gemma3:1b`).
- `sklearn_model`: Pipeline de scikit-learn con entrenamiento y endpoint de predicción. Registra en MLflow.
- `cnn_image`: Clasificador CNN pequeño que aplica tres filtros y clasifica imágenes en 3 clases.
- `gradio_frontend`: Interfaz Gradio que conecta los tres servicios.

Infraestructura:
- `infra/docker-compose.yml` para desarrollo local (incluye servidor MLflow).
- `infra/swarm-stack.yml` para despliegue en Docker Swarm (ejemplo mínimo).

Cada servicio incluye un `Dockerfile` y un `requirements.txt`. Las pruebas están en los directorios `tests/` de cada servicio.

Repositorio: `mlops-final-project`