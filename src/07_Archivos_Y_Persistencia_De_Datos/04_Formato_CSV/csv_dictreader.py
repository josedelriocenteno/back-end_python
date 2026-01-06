# csv_dictreader.py
# ==========================
# Lectura de CSV usando DictReader
# Cada fila se convierte en un diccionario {columna: valor}
# Muy útil para proyectos de backend y data pipelines

import csv
from pathlib import Path
from typing import Dict, Any, List

# ---------------------------------------------------------
# 1️⃣ Archivo CSV de ejemplo
# ---------------------------------------------------------
ruta_csv = Path("usuarios.csv")

# Contenido esperado:
# nombre,edad,hobby
# Juan,30,futbol
# Ana,25,pintura
# Luis,28,lectura

# ---------------------------------------------------------
# 2️⃣ Leer CSV con DictReader
# ---------------------------------------------------------
with ruta_csv.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)  # Crea diccionarios por fila
    
    for i, fila in enumerate(reader):
        print(f"Fila {i} como dict:", fila)
        # Acceso seguro
        nombre = fila.get("nombre", "Desconocido")
        edad_str = fila.get("edad", "0")
        hobby = fila.get("hobby", "")
        
        try:
            edad = int(edad_str)
        except ValueError:
            edad = 0
            print(f"Advertencia: Edad inválida en fila {i}: {edad_str}")
        
        print(f"{nombre} tiene {edad} años y le gusta {hobby}")

# ---------------------------------------------------------
# 3️⃣ Validación de filas
# ---------------------------------------------------------
# Función para validar estructura y tipos
def validar_fila_usuario(fila: Dict[str, Any]) -> Dict[str, Any]:
    # Verificar claves obligatorias
    required_keys = ["nombre", "edad", "hobby"]
    for key in required_keys:
        if key not in fila:
            raise ValueError(f"Falta clave '{key}' en fila: {fila}")
    
    # Validar tipos
    fila_validada = {}
    fila_validada["nombre"] = str(fila["nombre"])
    
    try:
        fila_validada["edad"] = int(fila["edad"])
    except (ValueError, TypeError):
        fila_validada["edad"] = 0  # Valor por defecto
        print(f"Advertencia: edad inválida, se asigna 0: {fila['edad']}")
    
    fila_validada["hobby"] = str(fila["hobby"])
    
    return fila_validada

# Leer y validar todas las filas
usuarios_validos: List[Dict[str, Any]] = []
with ruta_csv.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for fila in reader:
        try:
            usuario = validar_fila_usuario(fila)
            usuarios_validos.append(usuario)
        except ValueError as e:
            print(f"Fila ignorada por error: {e}")

print("\nUsuarios válidos procesados:")
for u in usuarios_validos:
    print(u)

# ---------------------------------------------------------
# 4️⃣ Buenas prácticas profesionales
# ---------------------------------------------------------
# ✅ Usar DictReader en lugar de reader para mayor claridad
# ✅ Validar claves y tipos en cada fila
# ✅ Manejar errores de conversión (edad, fechas, números)
# ✅ Definir valores por defecto si es seguro
# ✅ Manejar filas incompletas o corruptas con logging
# ✅ Mantener encoding="utf-8" y newline="" al abrir archivos
# ✅ Para grandes CSV, procesar en streaming (una fila a la vez)
# ✅ Separar lectura de CSV y lógica de negocio para modularidad

# ---------------------------------------------------------
# 5️⃣ Resumen
# ---------------------------------------------------------
# - csv.DictReader → convierte filas a diccionarios
# - Acceso por nombre de columna → más seguro y legible
# - Validar cada fila: claves, tipos, valores
# - Usar try/except para evitar que un error detenga todo el proceso
# - Guardar filas válidas en una lista o procesarlas directamente
# - Preparar los datos para backend, ML o data pipelines
