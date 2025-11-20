# Clasificador CNN de Imágenes

Aplica tres filtros (suavizado, detección de bordes y nitidez) y ejecuta una CNN pequeña para clasificación.

Ejecutar localmente:

```
python -m venv .venv; .venv\Scripts\activate; pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8002
```

Punto de acceso:
- `POST /classify` formulario multipart con archivo de imagen -> {predicted_class, probabilities, note}

Limitaciones: modelo de demostración pequeño; limitado a 3 clases y puede no generalizar.
