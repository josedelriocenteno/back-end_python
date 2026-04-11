# keyword_only_args.py
"""
PARÁMETROS SOLO POR PALABRA CLAVE (KEYWORD-ONLY ARGS)
======================================================

Objetivo:
- Entender cómo forzar que ciertos parámetros solo se pasen por nombre
- Mejorar la claridad y seguridad en APIs, funciones de backend y pipelines
- Evitar errores por confusión en el orden de los argumentos

Contexto:
- En Python, los parámetros que van después de un `*` en la definición
  solo pueden pasarse como argumentos nombrados.
- Esto es crucial en funciones con muchos parámetros opcionales o configurables.
"""

# =========================================================
# 1. Sintaxis básica
# =========================================================

def crear_usuario(nombre, *, rol="usuario", activo=True):
    """
    Los parámetros 'rol' y 'activo' solo se pueden pasar como keyword arguments
    """
    print(f"Nombre: {nombre}, Rol: {rol}, Activo: {activo}")

# Uso correcto
crear_usuario("Ana", rol="admin", activo=False)

# ❌ Uso incorrecto: pasar por posición generará TypeError
# crear_usuario("Ana", "admin", False)

# =========================================================
# 2. Mezcla con parámetros posicionales y *args/**kwargs
# =========================================================

def procesar_datos(a, b, *args, multiplicador=1, verbose=False, **kwargs):
    """
    - a, b → parámetros posicionales
    - *args → parámetros extra posicionales
    - multiplicador, verbose → solo por keyword
    - **kwargs → otros argumentos nombrados
    """
    total = (a + b + sum(args)) * multiplicador
    if verbose:
        print(f"Datos: a={a}, b={b}, args={args}, multiplicador={multiplicador}, extras={kwargs}")
    return total

resultado = procesar_datos(1, 2, 3, 4, multiplicador=2, verbose=True, extra="dato")
print("Resultado:", resultado)

# =========================================================
# 3. Beneficios en APIs y backend
# =========================================================

# - Claridad: quien llama la función sabe exactamente qué está configurando
# - Seguridad: evita que alguien rompa el flujo pasando parámetros en el orden incorrecto
# - Flexibilidad: parámetros opcionales múltiples sin confusión de posiciones
# - Muy útil para endpoints REST o funciones de pipelines de datos donde hay muchas opciones configurables

# Ejemplo: endpoint genérico de filtrado
def filtrar_registros(tabla, *, limite=10, ordenar_por="id", desc=False):
    """
    tabla → posicional
    limite, ordenar_por, desc → solo keyword
    """
    print(f"Filtrando {tabla}, límite={limite}, ordenar_por={ordenar_por}, descendente={desc}")

filtrar_registros("usuarios", limite=5, desc=True)

# =========================================================
# 4. Buenas prácticas
# =========================================================

# - Usa keyword-only args para parámetros opcionales importantes
# - Mantén consistencia en APIs y librerías: todos los parámetros configurables deben ser keyword-only
# - Documenta bien cada parámetro con docstrings
# - Evita abusar de *args para evitar confusión; combina con keyword-only args para claridad
# - Combina con **kwargs si necesitas extensibilidad futura sin romper la función
