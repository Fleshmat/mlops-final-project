# Clasificador CNN de Imágenes

Aplica tres filtros (suavizado, detección de bordes y nitidez) y ejecuta una CNN pequeña para clasificación.

Punto de acceso:
- `POST /classify` formulario multipart con archivo de imagen -> {predicted_class, probabilities, note}

Limitaciones: modelo de demostración pequeño; limitado a 4 clases.
