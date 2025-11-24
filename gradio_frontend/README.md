# Gradio Frontend

Propósito: Interfaz web (Gradio) que permite interactuar con los otros tres servicios:

- Chatear con el LLM (`llm_connector`).
- Enviar datos tabulares al modelo de `sklearn_model` para validación/predicción.
- Subir imágenes para clasificación con `cnn_image`.

Descripción de las funcionalidades / endpoints usados internamente:
- LLM: `POST {LLM_URL}` JSON {"question": "..."} -> {"answer": "..."}
- Sklearn: `POST {SKLEARN_URL}` JSON {"features": [f1, f2, ...]} -> {"prediction": [...]}
- CNN: `POST {CNN_URL}` multipart `file` -> {"predicted_class": "...", "probabilities": [...], "note": "..."}

Ejemplos de uso desde la UI:
- Chat LLM: escribir una pregunta y pulsar "Preguntar".
- Tabular: introducir valores y pulsar "Predecir".
- Imagen: subir imagen (JPG/PNG) y pulsar "Clasificar".

Notas y limitaciones visibles en la UI:
- La aplicación mostrará errores legibles cuando alguno de los servicios no sea accesible (p.ej. "LLM unreachable").
- El clasificador de imágenes es un ejemplo pequeño limitado a 4 clases (identificar numero del 0 al 3); su rendimiento real es limitado.
- Se usan timeouts para llamadas HTTP (configurables modificando `app.py`).
