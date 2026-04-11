# Poetry en Docker: El combo perfecto

Poetry es el estándar moderno para gestionar paquetes en Python, pero su integración con Docker requiere un par de trucos para no ensuciar la imagen y aprovechar la caché.

## 1. Instalación de Poetry en la imagen
No instales Poetry usando `pip install poetry` dentro del contenedor (puede dar conflictos de versiones). Usa el script oficial o instálalo de forma aislada.

## 2. Configuración Clave
Docker ya proporciona aislamiento, por lo que no necesitamos que Poetry cree un entorno virtual (`.venv`) dentro de la imagen. Esto ahorra espacio y simplifica las rutas.

```dockerfile
# Configuración senior para evitar virtualenvs dentro de Docker
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/tmp/poetry_cache'
```

## 3. Ejemplo de Dockerfile con Poetry (Optimizado)
```dockerfile
FROM python:3.11-slim

# Instalamos Poetry una sola vez
RUN pip install poetry==1.6.1

WORKDIR /app

# Copiamos SOLO los archivos de configuración primero
COPY pyproject.toml poetry.lock ./

# Instalamos dependencias SIN instalar el proyecto actual (--no-root)
# Esto permite cachear las librerías pesadas por separado del código.
RUN poetry install --no-interaction --no-ansi --no-root --only main

# Copiamos el código
COPY . .

# Instalamos el proyecto (ahora sí, con el código)
RUN poetry install --no-interaction --no-ansi --only main

CMD ["python", "-m", "mi_app.main"]
```

## 4. Por qué usar `--no-root`
En la primera fase de instalación, solo queremos las librerías externas (Pandas, FastAPI). Si no usas `--no-root`, Poetry intentará instalar tu carpeta de código actual, lo que invalidaría la caché de Docker en cada línea de código que cambies.

## Resumen: Predictibilidad Total
Usar Poetry con el archivo `poetry.lock` dentro de Docker garantiza que las versiones de las librerías en producción sean **idénticas** a las que usaste en desarrollo. Se acabó el "en mi máquina funciona con la versión 1.2 pero en el servidor falló porque se bajó la 1.3".
