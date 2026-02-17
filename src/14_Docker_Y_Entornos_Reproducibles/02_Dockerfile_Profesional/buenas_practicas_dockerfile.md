# Buenas Prácticas en Dockerfiles (Senior Guide)

Escribir un Dockerfile que "funcione" es fácil. Escribir uno eficiente, rápido y seguro requiere técnica. Aquí los principios del desarrollador senior.

## 1. El orden de los factores SÍ altera el producto
Docker guarda en caché cada línea (capa). Si cambias una línea, todas las de abajo se ejecutan de nuevo.
- **MAL:** Copiar todo el código y luego instalar librerías. Cada vez que cambies un `print`, se descargarán todas las librerías de nuevo.
- **BIEN:** Copiar `requirements.txt` -> Instalar -> Copiar el resto del código.

## 2. Usa imágenes 'slim' o 'alpine'
- `python:3.11`: (~900MB) Incluye herramientas innecesarias como compiladores, kits de C++, etc.
- `python:3.11-slim`: (~120MB) La base ideal. Basada en Debian pero limpia.
- `python:3.11-alpine`: (~45MB) Ultra-ligera basada en Alpine Linux. **⚠️ Cuidado:** Puede dar problemas con librerías que necesitan compilación de C (como Pandas o Psycopg2).

## 3. Combina los comandos `RUN`
Cada `RUN` crea una nueva capa de disco.
- **MAL:** 
  ```dockerfile
  RUN apt update
  RUN apt install git
  ```
- **BIEN:**
  ```dockerfile
  RUN apt update && apt install -y git && rm -rf /var/lib/apt/lists/*
  ```
- **Tip:** Limpiar la lista de apt en la misma línea reduce el tamaño de la capa.

## 4. Usa `.dockerignore`
Igual que el `.gitignore`, evita que archivos innecesarios suban a la imagen (como `.git`, `__pycache__`, carpetas de tests o archivos `.env` con secretos locales).
- **Resultado:** Build más rápido y menos riesgo de seguridad.

## 5. El comando `CMD` siempre en formato lista
- **MAL:** `CMD python main.py` (Lanza el proceso a través de un shell `/bin/sh`, lo que impide que el contenedor reciba señales de apagado correctamente).
- **BIEN:** `CMD ["python", "main.py"]` (Ejecución directa).

## Resumen: Rapidez y Seguridad
Un Dockerfile senior es aquel que se construye en segundos (buen uso de caché), es lo más pequeño posible (menos superficie de ataque) y no corre con privilegios innecesarios.
