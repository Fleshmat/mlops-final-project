# Conector LLM

Propósito: Reenviar consultas a una instancia Ollama (modelo por defecto `gemma3:1b`).

Ejecutar localmente (supone que Ollama está activo o accesible mediante `OLLAMA_URL`):

```
python -m venv .venv; .venv\Scripts\activate; pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Variables de entorno:
- `OLLAMA_URL` por ejemplo `http://localhost:11434` o `http://llama3_2:11434` en Docker Compose.
- `OLLAMA_MODEL` por defecto `gemma3:1b`.
- `LOG_LEVEL` por defecto `INFO`.

Opciones Docker Compose:
- `LLAMA_IMAGE` (opcional): establecer la imagen Docker que servirá Llama 3.2. Ejemplo: `LLAMA_IMAGE=ghcr.io/tu-organizacion/gemma3:1b` (reemplaza por la imagen oficial que vayas a usar).

Punto de acceso:
- `POST /query` JSON: {"question": "...", "history": [...]} -> {"answer": "..."}
