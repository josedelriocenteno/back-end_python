"""
streaming_archivos.py
=====================

PROCESAMIENTO DE ARCHIVOS GRANDES SIN CARGAR TODO EN RAM
---------------------------------------------------------

Objetivo:
---------
Aprender a manejar archivos que no caben completamente en memoria, usando:
- Iteradores y generadores
- Lectura línea por línea
- Lectura por bloques
- Buenas prácticas de manejo de recursos

Esto es esencial en Data, ML y pipelines de backend que procesan datasets enormes.

Conceptos clave:
----------------
1. Nunca uses `read()` con archivos gigantes: podrías saturar la RAM.
2. Python permite iterar directamente sobre un archivo línea por línea.
3. Para binarios grandes, se recomienda leer en **chunks**.
4. Usar `with` para asegurarnos que los archivos se cierren correctamente.
"""

from pathlib import Path

# ============================================================
# 1️⃣ DEFINIR RUTA DE ARCHIVO
# ============================================================

ARCHIVO_GRANDE = Path("data/gran_dataset.csv")

# ============================================================
# 2️⃣ LECTURA LÍNEA POR LÍNEA (STREAMING)
# ============================================================

def procesar_linea_por_linea(ruta: Path) -> None:
    """
    Itera sobre cada línea del archivo sin cargar todo en memoria.
    
    Args:
        ruta (Path): Ruta del archivo a procesar.
    """
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")

    # El 'with' garantiza que el archivo se cierre correctamente
    with ruta.open("r", encoding="utf-8") as f:
        for numero_linea, linea in enumerate(f, start=1):
            # Procesamiento de cada línea
            linea = linea.strip()  # eliminar saltos de línea
            if linea:  # ignorar líneas vacías
                print(f"Línea {numero_linea}: {linea}")


# ============================================================
# 3️⃣ LECTURA POR BLOQUES (CHUNKS) PARA BINARIOS
# ============================================================

def procesar_binario_por_bloques(ruta: Path, tamano_bloque: int = 1024) -> None:
    """
    Procesa un archivo binario en bloques de tamaño fijo.
    
    Args:
        ruta (Path): Ruta del archivo binario.
        tamano_bloque (int): Número de bytes a leer por iteración.
    """
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")

    with ruta.open("rb") as f:
        bloque_numero = 0
        while True:
            bloque = f.read(tamano_bloque)
            if not bloque:
                break  # fin del archivo
            bloque_numero += 1
            # Aquí podrías procesar el bloque (decodificar, parsear, etc.)
            print(f"Procesando bloque {bloque_numero}, tamaño: {len(bloque)} bytes")


# ============================================================
# 4️⃣ GENERADOR PERSONALIZADO PARA STREAMING
# ============================================================

def generador_lineas(ruta: Path):
    """
    Generador que yield línea por línea, eficiente para pipelines de ML/Data.
    
    Uso:
        for linea in generador_lineas(ARCHIVO_GRANDE):
            procesar(linea)
    """
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")

    with ruta.open("r", encoding="utf-8") as f:
        for linea in f:
            yield linea.strip()


# ============================================================
# 5️⃣ EJEMPLO DE USO
# ============================================================

def ejemplo_completo():
    """
    Flujo completo de streaming:
    1. Procesar línea por línea
    2. Procesar en bloques binarios
    3. Iterar con generador
    """
    print("➡️ Procesamiento línea por línea")
    procesar_linea_por_linea(ARCHIVO_GRANDE)

    print("\n➡️ Procesamiento por bloques (1024 bytes)")
    procesar_binario_por_bloques(ARCHIVO_GRANDE, tamano_bloque=1024)

    print("\n➡️ Uso de generador")
    for i, linea in enumerate(generador_lineas(ARCHIVO_GRANDE), start=1):
        print(f"Línea {i}: {linea}")
        if i >= 5:  # mostrar solo las primeras 5 líneas para el ejemplo
            break


# ============================================================
# 6️⃣ EJECUTAR
# ============================================================

if __name__ == "__main__":
    ejemplo_completo()
