"""
ejercicios_archivos.py
======================

Casos reales de manipulación de archivos y persistencia:
- CSV
- JSON
- Parquet

Objetivo:
---------
Practicar lectura, escritura, validación y limpieza de datos
usando los formatos más comunes en Python.
"""

import json
import csv
from pathlib import Path
import tempfile
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

# -----------------------------------------------------------
# 1️⃣ Ejercicio CSV: Guardar y leer datos de usuarios
# -----------------------------------------------------------

# Datos de ejemplo
usuarios = [
    {"nombre": "Ana", "edad": 28, "email": "ana@email.com"},
    {"nombre": "Luis", "edad": 32, "email": "luis@email.com"},
    {"nombre": "Marta", "edad": 24, "email": "marta@email.com"},
]

# 1.a. Guardar CSV
csv_path = Path("usuarios.csv")
with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["nombre", "edad", "email"])
    writer.writeheader()  # Escribe la fila de cabecera
    for usuario in usuarios:
        writer.writerow(usuario)

print(f"CSV guardado en: {csv_path.resolve()}")

# 1.b. Leer CSV y validar emails
with csv_path.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for fila in reader:
        nombre, email = fila["nombre"], fila["email"]
        assert "@" in email, f"Email inválido: {email}"  # Validación básica
        print(f"Usuario {nombre} con email {email} es válido.")

# -----------------------------------------------------------
# 2️⃣ Ejercicio JSON: Configuración de proyecto
# -----------------------------------------------------------

config = {
    "project_name": "IA_Data",
    "version": "1.0.0",
    "authors": ["Carlos", "Lucia"],
    "settings": {"debug": True, "max_retries": 3},
}

# Guardar configuración JSON
json_path = Path("config.json")
with json_path.open("w", encoding="utf-8") as f:
    json.dump(config, f, indent=4)

# Leer y modificar configuración
with json_path.open("r", encoding="utf-8") as f:
    cfg = json.load(f)

cfg["settings"]["debug"] = False  # Cambiamos un valor
print("Configuración modificada:", cfg)

# -----------------------------------------------------------
# 3️⃣ Ejercicio Archivos Temporales CSV
# -----------------------------------------------------------
"""
Simulamos procesamiento de datos sin escribir archivos permanentes.
"""

with tempfile.NamedTemporaryFile(mode="w+", newline="", delete=True) as tmp:
    writer = csv.DictWriter(tmp, fieldnames=["nombre", "edad"])
    writer.writeheader()
    for u in usuarios:
        writer.writerow({"nombre": u["nombre"], "edad": u["edad"]})
    
    tmp.seek(0)
    print("Contenido CSV temporal:")
    print(tmp.read())

# -----------------------------------------------------------
# 4️⃣ Ejercicio Parquet: Almacenamiento columnar eficiente
# -----------------------------------------------------------

# Convertimos la lista de usuarios en DataFrame de pandas
df = pd.DataFrame(usuarios)

# Guardar en Parquet
parquet_path = Path("usuarios.parquet")
df.to_parquet(parquet_path, engine="pyarrow", index=False)
print(f"Archivo Parquet guardado en: {parquet_path.resolve()}")

# Leer Parquet
df_leido = pd.read_parquet(parquet_path, engine="pyarrow")
print("Usuarios leídos desde Parquet:")
print(df_leido)

# Validación sencilla
assert len(df_leido) == len(usuarios), "Número de filas incorrecto"

# -----------------------------------------------------------
# 5️⃣ Buenas prácticas aplicadas en todos los ejercicios
# -----------------------------------------------------------
"""
1. Usar context managers para abrir archivos (con 'with') → evita fugas de recursos.
2. Validar datos al leer: emails, tipos de datos, número de filas, etc.
3. Para CSV grandes → considerar streaming o iteradores.
4. Para datos temporales → usar tempfile para no llenar disco con archivos intermedios.
5. Para Parquet → ideal para grandes volúmenes y análisis columnar eficiente.
6. Mantener consistencia de codificación (UTF-8).
7. Documentar el flujo de datos y formatos para reproducibilidad.
"""

# -----------------------------------------------------------
# 6️⃣ Desafío final (integrado)
# -----------------------------------------------------------
"""
Objetivo: Crear un pipeline de persistencia completo:
1. Guardar usuarios en CSV y JSON.
2. Procesar temporalmente los datos.
3. Convertir a Parquet para análisis posterior.
4. Validar integridad y limpiar archivos temporales automáticamente.
"""

def pipeline_persistencia(usuarios: list[dict]):
    # CSV temporal
    with tempfile.NamedTemporaryFile(mode="w+", newline="", delete=True) as tmp_csv:
        writer = csv.DictWriter(tmp_csv, fieldnames=["nombre", "edad"])
        writer.writeheader()
        for u in usuarios:
            writer.writerow({"nombre": u["nombre"], "edad": u["edad"]})
        tmp_csv.seek(0)
        print("CSV temporal procesado:")
        print(tmp_csv.read())

    # JSON persistente
    with open("usuarios_pipeline.json", "w", encoding="utf-8") as f_json:
        json.dump(usuarios, f_json, indent=2)

    # Parquet persistente
    df = pd.DataFrame(usuarios)
    df.to_parquet("usuarios_pipeline.parquet", engine="pyarrow", index=False)

    # Validaciones
    df_leido = pd.read_parquet("usuarios_pipeline.parquet")
    assert len(df_leido) == len(usuarios), "Pipeline error: filas inconsistentes"
    print("Pipeline completado con éxito y datos validados.")

pipeline_persistencia(usuarios)
