"""
archivos_en_api.py
==================

UPLOAD / DOWNLOAD DE ARCHIVOS EN BACKEND
----------------------------------------

Objetivo:
---------
Aprender a implementar endpoints para subir y descargar archivos en un API de manera segura,
eficiente y profesional, aplicable en proyectos de backend y pipelines de datos.

Conceptos clave:
----------------
1. Validar los archivos recibidos (tipo, tamaño, extensión).
2. Guardar archivos de manera organizada en disco o almacenamiento cloud.
3. Descargar archivos de forma segura y controlada.
4. Evitar path traversal y riesgos de seguridad.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import shutil

app = FastAPI()

# ============================================================
# 1️⃣ RUTAS DE ALMACENAMIENTO
# ============================================================

UPLOAD_DIR = Path("uploads/")
UPLOAD_DIR.mkdir(exist_ok=True)  # crear carpeta si no existe

# ============================================================
# 2️⃣ UPLOAD DE ARCHIVOS
# ============================================================

@app.post("/upload/")
async def subir_archivo(archivo: UploadFile = File(...)):
    """
    Endpoint para subir un archivo.

    Args:
        archivo (UploadFile): Archivo enviado en la request.

    Returns:
        dict: Confirmación y nombre de archivo guardado.
    """
    # Validación básica de seguridad: evitar path traversal
    if ".." in archivo.filename or archivo.filename.startswith("/"):
        raise HTTPException(status_code=400, detail="Nombre de archivo inválido")

    # Validar extensión (ejemplo: solo CSV o TXT)
    if not archivo.filename.endswith((".csv", ".txt")):
        raise HTTPException(status_code=400, detail="Extensión no permitida")

    # Guardar el archivo en disco
    destino = UPLOAD_DIR / archivo.filename
    with destino.open("wb") as f:
        shutil.copyfileobj(archivo.file, f)

    return {"mensaje": "Archivo subido con éxito", "archivo": archivo.filename}

# ============================================================
# 3️⃣ DOWNLOAD DE ARCHIVOS
# ============================================================

@app.get("/download/{nombre_archivo}")
async def descargar_archivo(nombre_archivo: str):
    """
    Endpoint para descargar un archivo previamente subido.

    Args:
        nombre_archivo (str): Nombre del archivo a descargar.

    Returns:
        FileResponse: Archivo para la descarga.
    """
    # Evitar path traversal
    if ".." in nombre_archivo or nombre_archivo.startswith("/"):
        raise HTTPException(status_code=400, detail="Nombre de archivo inválido")

    archivo_path = UPLOAD_DIR / nombre_archivo
    if not archivo_path.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return FileResponse(path=archivo_path, filename=archivo_path.name)

# ============================================================
# 4️⃣ EJEMPLO DE USO
# ============================================================

"""
Para probar:
1. Ejecutar:
    uvicorn archivos_en_api:app --reload

2. Subir archivo:
   POST a /upload/ usando Swagger UI o Postman con un CSV o TXT.

3. Descargar archivo:
   GET a /download/nombre_del_archivo

Notas:
- Siempre validar tamaño y tipo de archivo en producción.
- Considerar almacenamiento en cloud (S3, GCS) si los archivos son grandes o persistentes.
- Logging de uploads/downloads para auditoría.
"""
