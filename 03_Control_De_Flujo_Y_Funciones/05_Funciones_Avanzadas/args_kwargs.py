# args_kwargs.py
"""
USO DE *ARGS Y **KWARGS EN PYTHON
=================================

Objetivo:
- Dominar el paso de argumentos posicionales y nombrados flexibles
- Saber cuándo y cómo usar *args y **kwargs correctamente
- Aplicable a funciones de backend, APIs, pipelines y procesamiento de datos

Contexto:
- *args permite pasar cualquier número de argumentos posicionales
- **kwargs permite pasar cualquier número de argumentos nombrados
- Son esenciales para funciones genéricas, wrappers, decorators y librerías
"""

# =========================================================
# 1. Uso básico de *args
# =========================================================

def sumar_todos(*args):
    """
    Suma todos los argumentos posicionales pasados
    Ejemplo: sumar_todos(1,2,3) -> 6
    """
    total = 0
    for num in args:
        total += num
    return total

print(sumar_todos(1, 2, 3))          # 6
print(sumar_todos(5, 10, 15, 20))    # 50

# Nota: args se recibe como una tupla
def mostrar_tipo(*args):
    print(type(args))  # <class 'tuple'>
    print(args)

mostrar_tipo(1, 2, 3)

# =========================================================
# 2. Uso básico de **kwargs
# =========================================================

def imprimir_info_usuario(**kwargs):
    """
    Recibe cualquier número de argumentos nombrados
    Ejemplo: imprimir_info_usuario(nombre="Ana", edad=25)
    """
    for clave, valor in kwargs.items():
        print(f"{clave}: {valor}")

imprimir_info_usuario(nombre="Luis", rol="admin", activo=True)

# Nota: kwargs se recibe como un diccionario
def mostrar_tipo_kwargs(**kwargs):
    print(type(kwargs))  # <class 'dict'>
    print(kwargs)

mostrar_tipo_kwargs(a=1, b=2)

# =========================================================
# 3. Mezcla de argumentos normales, *args y **kwargs
# =========================================================

def crear_usuario(nombre, *args, rol="usuario", **kwargs):
    """
    Ejemplo de mezcla:
    - nombre: obligatorio
    - args: posiciones adicionales (teléfonos, códigos, etc.)
    - rol: argumento nombrado con valor por defecto
    - kwargs: cualquier otro dato extra
    """
    print("Nombre:", nombre)
    print("Args:", args)
    print("Rol:", rol)
    print("Extras:", kwargs)

crear_usuario("Ana", 123, 456, rol="admin", activo=True, ciudad="Madrid")

# =========================================================
# 4. Usos prácticos en backend/data pipelines
# =========================================================

# 4.1 Wrapper para logging de funciones
def log_wrapper(func):
    def wrapper(*args, **kwargs):
        print(f"Llamando {func.__name__} con args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper

@log_wrapper
def procesar_datos(a, b, metodo="sum"):
    if metodo == "sum":
        return a + b
    return a * b

resultado = procesar_datos(5, 10, metodo="sum")  # logging automático

# 4.2 Función genérica para endpoints de APIs
def construir_respuesta(status, *args, **kwargs):
    """
    Construye diccionario genérico para respuesta JSON en backend
    """
    respuesta = {"status": status, "data": args}
    respuesta.update(kwargs)
    return respuesta

resp = construir_respuesta("OK", {"id": 1}, {"id": 2}, total=2, page=1)
print(resp)

# =========================================================
# 5. Buenas prácticas
# =========================================================

# - Siempre documentar qué tipo de datos espera *args y **kwargs
# - Evitar abusar: si la función es compleja, es mejor usar parámetros explícitos
# - *args para listas o tuplas de valores, **kwargs para opciones configurables
# - Mantener orden: parámetros normales, luego *args, luego parámetros por defecto nombrados, luego **kwargs
# - Útil para wrappers, decorators, funciones genéricas, APIs, pipelines y pruebas unitarias
