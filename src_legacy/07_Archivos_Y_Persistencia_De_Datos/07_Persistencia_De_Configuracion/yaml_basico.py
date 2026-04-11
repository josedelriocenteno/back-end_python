"""
yaml_basico.py
===============

GESTIÓN DE CONFIGURACIÓN Y DATOS CON YAML EN PYTHON
---------------------------------------------------

Este archivo explica:
1. Qué es YAML y por qué se usa en proyectos profesionales.
2. Cómo se diferencia de INI y .env.
3. Cómo leer y escribir YAML desde Python correctamente.
4. Buenas prácticas, errores comunes y recomendaciones reales de producción.
"""

# ============================================================
# 1. POR QUÉ YAML
# ============================================================
#
# Problema:
# - .env → bueno para secretos simples
# - INI → bueno para configuraciones estructuradas pequeñas
#
# Pero en proyectos de ML, Data o Backend, necesitamos:
# - Estructuras complejas (listas, diccionarios anidados)
# - Legibilidad humana
# - Serialización clara para pipelines, configs, experimentos
#
# Solución: YAML
# - Formato legible, jerárquico
# - Compatible con Python (dicts, lists, str, int, bool)
# - Muy usado en ML, infra y pipelines
# ============================================================

# ============================================================
# 2. DIFERENCIAS CLAVE CON INI y .env
# ============================================================
#
# .env:
# - Solo pares clave=valor
# - Secretos simples
#
# INI:
# - Secciones + clave=valor
# - No soporta listas o dicts complejos
#
# YAML:
# - Listas, dicts anidados
# - Tipos de datos reales
# - Comentarios
# ============================================================


# ============================================================
# 3. LIBRERÍA PYTHON
# ============================================================
# Python no trae YAML nativo
# Usamos: PyYAML
# pip install pyyaml
# ============================================================

import yaml
from pathlib import Path


# ============================================================
# 4. EJEMPLO DE ARCHIVO YAML
# ============================================================

"""
app_config.yaml

database:
  host: localhost
  port: 5432
  user: app_user
  password: secret

app:
  debug: true
  name: MiAplicacion
  features:
    - login
    - dashboard
    - reporting

ml_pipeline:
  batch_size: 64
  epochs: 10
  seed: 42
"""

# ============================================================
# 5. RUTA DEL ARCHIVO YAML
# ============================================================

CONFIG_PATH = Path("config/app_config.yaml")


# ============================================================
# 6. LEER YAML
# ============================================================

def cargar_yaml(ruta: Path) -> dict:
    """
    Lee un archivo YAML y devuelve un diccionario Python.
    """
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")

    with ruta.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)  # safe_load evita ejecución de código arbitrario
    return data


# ============================================================
# 7. ACCEDER A DATOS
# ============================================================

def mostrar_datos_basicos(config: dict) -> None:
    """
    Muestra cómo acceder a valores básicos y estructuras complejas.
    """
    db_host = config["database"]["host"]
    db_port = config["database"]["port"]
    debug = config["app"]["debug"]
    features = config["app"]["features"]
    batch_size = config["ml_pipeline"]["batch_size"]

    print("Host DB:", db_host)
    print("Puerto DB:", db_port)
    print("Debug:", debug)
    print("Features:", features)
    print("Batch size ML:", batch_size)


# ============================================================
# 8. ESCRIBIR YAML
# ============================================================

def guardar_yaml(ruta: Path, datos: dict) -> None:
    """
    Escribe un diccionario Python a YAML.
    """
    with ruta.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            datos,
            f,
            default_flow_style=False,  # hace legible, no todo en línea
            sort_keys=False,           # respeta el orden que pusimos
        )


# ============================================================
# 9. ERRORES COMUNES
# ============================================================

# ❌ Mal: usar yaml.load() sin safe_load → riesgo de ejecución de código
# ❌ Mal: no validar existencia del archivo
# ❌ Mal: asumir tipos → YAML soporta bool/int/list, siempre validar

# ✅ Siempre safe_load
# ✅ Validar keys y tipos
# ✅ Separar archivos por entorno o por pipeline


# ============================================================
# 10. EJEMPLO COMPLETO DE USO
# ============================================================

def ejemplo_completo():
    # 1. Cargar configuración
    config = cargar_yaml(CONFIG_PATH)

    # 2. Mostrar datos
    mostrar_datos_basicos(config)

    # 3. Modificar datos (ejemplo)
    config["app"]["debug"] = False
    config["ml_pipeline"]["epochs"] = 20

    # 4. Guardar cambios
    guardar_yaml(CONFIG_PATH, config)


if __name__ == "__main__":
    ejemplo_completo()
