# closures_casos_uso.py
"""
CLOSURES: CASOS DE USO PROFESIONALES
====================================

Objetivo:
- Demostrar cómo aplicar closures en configuraciones, validadores y factories
- Mejorar la modularidad, testabilidad y mantenimiento del código backend
- Evitar variables globales y mantener estado de manera segura
"""

# =========================================================
# 1. Closure para configuración de funciones
# =========================================================

def configurar_saludo(prefijo: str):
    """
    Closure que encapsula configuración de saludo
    Útil en APIs o microservicios que requieren personalización
    """
    def saludar(nombre: str):
        return f"{prefijo} {nombre}"
    return saludar

hola = configurar_saludo("Hola")
print(hola("Carlos"))  # Hola Carlos
buenos_dias = configurar_saludo("Buenos días")
print(buenos_dias("Ana"))  # Buenos días Ana

# =========================================================
# 2. Closure para validadores de datos
# =========================================================

def validador_edad(min_edad: int):
    """
    Crea un validador de edad mínimo usando closure
    Aplicable en endpoints de registro o formularios
    """
    def validar(edad: int):
        if edad < min_edad:
            raise ValueError(f"La edad debe ser >= {min_edad}")
        return True
    return validar

validar_18 = validador_edad(18)
print(validar_18(20))  # True
# print(validar_18(16))  # ValueError: La edad debe ser >= 18

# =========================================================
# 3. Closure como factory de funciones
# =========================================================

def factory_operaciones(factor: int):
    """
    Devuelve funciones de multiplicación personalizadas
    Útil en pipelines para transformaciones parametrizadas
    """
    def multiplicar(x: int):
        return x * factor

    def dividir(x: int):
        return x / factor

    return multiplicar, dividir

mult_3, div_3 = factory_operaciones(3)
print(mult_3(10))  # 30
print(div_3(30))   # 10.0

# =========================================================
# 4. Uso de closures en pipelines de datos
# =========================================================

def crear_logger(stage_name: str):
    """
    Cada stage en un pipeline puede tener su logger privado
    """
    contador = 0

    def log(data):
        nonlocal contador
        contador += 1
        print(f"[{stage_name}] Ejecución #{contador}: {data}")
        return data  # pipeline sigue funcionando normalmente

    return log

logger_etl = crear_logger("ETL")
logger_etl({"id": 1})  # [ETL] Ejecución #1: {'id': 1}
logger_etl({"id": 2})  # [ETL] Ejecución #2: {'id': 2}

# =========================================================
# 5. Buenas prácticas
# =========================================================
# - Documentar qué variables externas captura cada closure
# - Usar closures para mantener estado pequeño y encapsulado
# - Evitar closures demasiado complejas; considerar clases si hay muchas responsabilidades
# - Ideal para:
#   - Validaciones parametrizadas
#   - Configuración de endpoints
#   - Factories de funciones reutilizables
#   - Logging y contadores en pipelines
