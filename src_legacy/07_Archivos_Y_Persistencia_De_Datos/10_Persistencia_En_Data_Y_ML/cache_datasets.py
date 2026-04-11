"""
cache_datasets.py
=================

OBJETIVO
--------
Proveer un sistema simple de caching para datasets, permitiendo:
- Reutilizar datos ya cargados en memoria o en disco
- Evitar recargar datasets grandes desde archivos repetidamente
- Mantener reproducibilidad y consistencia en proyectos de Data/ML

TODO explicado paso a paso, sin asumir conocimientos previos.
"""

from pathlib import Path
import pandas as pd
import json
import pickle
from typing import Optional, Any, Dict

# ============================================================
# 1️⃣ Carpeta de cache
# ============================================================
BASE_DIR = Path(__file__).parent
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)  # Crear si no existe

# ============================================================
# 2️⃣ Cache en memoria
# ============================================================
# Diccionario global para almacenar datasets cargados
_mem_cache: Dict[str, Any] = {}

def cache_set(nombre: str, data: Any):
    """
    Guarda un objeto en la cache en memoria
    """
    _mem_cache[nombre] = data
    print(f"[Cache] Guardado en memoria: {nombre}")

def cache_get(nombre: str) -> Optional[Any]:
    """
    Recupera un objeto de la cache en memoria
    """
    data = _mem_cache.get(nombre)
    if data is not None:
        print(f"[Cache] Recuperado de memoria: {nombre}")
    return data

# ============================================================
# 3️⃣ Cache persistente en disco
# ============================================================
def cache_path(nombre: str, extension: str = ".pkl") -> Path:
    """
    Devuelve la ruta de archivo de cache correspondiente
    """
    return CACHE_DIR / f"{nombre}{extension}"

def guardar_cache_disco(nombre: str, data: Any, usar_pickle: bool = True):
    """
    Guarda un objeto en disco para reutilización futura
    """
    path = cache_path(nombre, ".pkl" if usar_pickle else ".json")
    
    if usar_pickle:
        # Pickle para objetos Python arbitrarios
        with path.open("wb") as f:
            pickle.dump(data, f)
        print(f"[Cache] Guardado en disco con pickle: {path}")
    else:
        # JSON para estructuras tipo dict/list
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[Cache] Guardado en disco como JSON: {path}")

def cargar_cache_disco(nombre: str, usar_pickle: bool = True) -> Optional[Any]:
    """
    Carga un objeto previamente guardado en disco
    """
    path = cache_path(nombre, ".pkl" if usar_pickle else ".json")
    if not path.exists():
        print(f"[Cache] No existe cache en disco: {path}")
        return None
    
    try:
        if usar_pickle:
            with path.open("rb") as f:
                data = pickle.load(f)
        else:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        print(f"[Cache] Cargado desde disco: {path}")
        return data
    except Exception as e:
        print(f"[Cache] Error cargando cache: {path} | Detalle: {e}")
        return None

# ============================================================
# 4️⃣ Uso combinado: memoria primero, disco después
# ============================================================
def obtener_dataset(nombre: str, cargar_funcion: Optional[callable] = None, usar_pickle: bool = True) -> Optional[Any]:
    """
    Devuelve un dataset usando cache:
    1. Intenta memoria
    2. Intenta disco
    3. Si no existe y se provee cargar_funcion, carga con ella y guarda en cache
    """
    # 1️⃣ Memoria
    data = cache_get(nombre)
    if data is not None:
        return data

    # 2️⃣ Disco
    data = cargar_cache_disco(nombre, usar_pickle=usar_pickle)
    if data is not None:
        cache_set(nombre, data)  # guardar también en memoria
        return data

    # 3️⃣ Cargar desde fuente externa
    if cargar_funcion is not None:
        print(f"[Cache] Dataset no encontrado, cargando con función externa: {nombre}")
        data = cargar_funcion()
        if data is not None:
            cache_set(nombre, data)
            guardar_cache_disco(nombre, data, usar_pickle=usar_pickle)
        return data
    
    print(f"[Cache] Dataset no disponible: {nombre}")
    return None

# ============================================================
# 5️⃣ Ejemplo completo de uso
# ============================================================
if __name__ == "__main__":
    # Ejemplo de función de carga externa
    def cargar_datos_simulados():
        import pandas as pd
        return pd.DataFrame({
            "id": [1,2,3],
            "valor": [10, 20, 30]
        })
    
    # Obtener dataset (memoria → disco → función)
    df = obtener_dataset("simulado", cargar_funcion=cargar_datos_simulados)
    print(df)

    # Guardar directamente en memoria y disco
    df_nuevo = pd.DataFrame({
        "id": [4,5,6],
        "valor": [40, 50, 60]
    })
    cache_set("nuevo_dataset", df_nuevo)
    guardar_cache_disco("nuevo_dataset", df_nuevo)

    # Recuperar dataset guardado
    df_recuperado = obtener_dataset("nuevo_dataset")
    print(df_recuperado)
