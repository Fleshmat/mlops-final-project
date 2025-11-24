# Conector LLM

Propósito: Reenviar consultas a una instancia Ollama (modelo por defecto `gemma3:1b`).

Ejecutar localmente (supone que Ollama está activo o accesible mediante `OLLAMA_URL`):

Punto de acceso:
- `POST /query` JSON: {"question": "...", "history": [...]} -> {"answer": "..."}
