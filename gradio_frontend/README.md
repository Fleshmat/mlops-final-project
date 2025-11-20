# Gradio Frontend

Propósito: Interfaz web (Gradio) que permite interactuar con los otros tres servicios:

- Chatear con el LLM (`llm_connector`).
- Enviar datos tabulares al modelo de `sklearn_model` para validación/predicción.
- Subir imágenes para clasificación con `cnn_image`.

Autor: Auto-generated
Fecha: 2025-11-18

Cómo ejecutar localmente:

1. Asegúrate de tener los servicios backend corriendo (por ejemplo con Docker Compose desde `infra/`).
2. Desde la carpeta `gradio_frontend` instala dependencias y ejecuta:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Variables de entorno relevantes:
- `LLM_URL` (por defecto `http://llm_connector:8000/query`) — endpoint del conector LLM.
- `SKLEARN_URL` (por defecto `http://sklearn_model:8001/predict`) — endpoint de predicción tabular.
- `CNN_URL` (por defecto `http://cnn_image:8002/classify`) — endpoint de clasificación de imágenes.

Descripción de las funcionalidades / endpoints usados internamente:
- LLM: `POST {LLM_URL}` JSON {"question": "..."} -> {"answer": "..."}
- Sklearn: `POST {SKLEARN_URL}` JSON {"features": [f1, f2, ...]} -> {"prediction": [...]}
- CNN: `POST {CNN_URL}` multipart `file` -> {"predicted_class": "...", "probabilities": [...], "note": "..."}

Ejemplos de uso desde la UI:
- Chat LLM: escribir una pregunta y pulsar "Ask".
- Tabular: introducir valores separados por comas (ej: `5.1,3.5,1.4,0.2`) y pulsar "Predict".
- Imagen: subir imagen (JPG/PNG) y pulsar "Classify".

Notas y limitaciones visibles en la UI:
- La aplicación mostrará errores legibles cuando alguno de los servicios no sea accesible (p.ej. "LLM unreachable").
- El clasificador de imágenes es un ejemplo pequeño limitado a 3 clases; su rendimiento real es limitado y no debe usarse en producción sin reentrenamiento y dataset adecuado.
- Se usan timeouts para llamadas HTTP (configurables modificando `app.py`).

Buenas prácticas y seguridad:
- No almacenar credenciales en código — usar variables de entorno.
- Para producción, proteger la interfaz con autenticación y colocar los backends detrás de un gateway seguro.

Preguntas frecuentes (rápido):
- ¿Necesito Ollama local? No, puedes apuntar `LLM_URL` a un Ollama remoto si está disponible; sin embargo, para mayor control se recomienda una instancia local.
