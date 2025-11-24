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

---

## Archivo `.env` y variables de entorno (ubicación y ejemplo)

Donde ubicar el archivo `.env`:
- Coloca el archivo `.env` **dentro de la carpeta `infra/`** (junto al `docker-compose.yml`). Docker Compose leerá automáticamente este archivo y lo usará para reemplazar variables en el archivo compose.

Ejemplo de estructura y contenido de `infra/.env`:

```

# Modelo Llama que usará el conector LLM
OLLAMA_MODEL=gemma3:1b
# URL del runtime que sirve Llama dentro de la red de Compose (no tocar si corresponde)
OLLAMA_URL=http://ollama:11434
# Nivel de logs estructurados
LOG_LEVEL=INFO
# URL para las peticiones al LLM
LLM_URL=http://llm_connector:8000/query
# URL donde Sklearn recibirá las peticiones
SKLEARN_URL=http://sklearn_model:8001/predict
# URL donde la red neuronal convolucional de Pytorch recibirá las peticiones
CNN_URL=http://cnn_image:8002/classify
# Dirección del servidor de seguimiento de MLflow
MLFLOW_TRACKING_URI=http://mlflow:5000
# Direccion en el contenedor donde se guardará y cargará el modelo de Sklearn
MODEL_PATH=skmodels/sklearn_model.pkl
# Direccion en el contenedor donde se guardará y cargará el modelo de Pytorch
CNN_MODEL_PATH=cnnmodels/cnn_mnist.pt
# Direccion donde se guardará el dataset del modelo de Sklearn
DATA_DIR=/data/
# Dataset seleccionado para el modelo de Sklearn
KAGGLE_DATASET=umuttuygurr/e-commerce-fraud-detection-dataset
# Usuario de Kaggle para la autenticacion
KAGGLE_USERNAME=tu_usuario_kaggle
# Llave de Kaggle para la autenticacion
KAGGLE_KEY=tu_llave_kaggle
# Lugar donde Mlflow guadará los registros
MLFLOW_BACKEND_STORE_URI=sqlite:///mlflow.db
# Lugar donde Mlflow guardará los artefactos
MLFLOW_DEFAULT_ARTIFACT_ROOT=/mlflow/artifacts

```


