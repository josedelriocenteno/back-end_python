# parametros_y_argumentos.py
"""
PARÁMETROS Y ARGUMENTOS EN PYTHON
=================================

Objetivo:
- Entender la diferencia entre parámetros posicionales y nombrados
- Saber cómo pasar argumentos correctamente
- Aplicable a backend, APIs y funciones de procesamiento de datos
"""

# =========================================================
# 1. Parámetros posicionales
# =========================================================

def saludar(nombre, edad):
    print(f"Hola {nombre}, tienes {edad} años.")

saludar("Ana", 25)  # Posicional: nombre="Ana", edad=25

# ❌ Error común: cambiar el orden de los parámetros
# saludar(25, "Ana")  # Resultado incorrecto

# =========================================================
# 2. Parámetros nombrados (keyword arguments)
# =========================================================

saludar(nombre="Luis", edad=30)  # Más legible
saludar(edad=30, nombre="Luis")  # Orden no importa con nombres

# =========================================================
# 3. Mezcla de posicional y nombrado
# =========================================================

saludar("Marta", edad=22)  # Primer parámetro posicional, segundo nombrado

# =========================================================
# 4. Parámetros por defecto
# =========================================================

def registrar_usuario(nombre, rol="usuario"):
    print(f"Registrando {nombre} con rol {rol}")

registrar_usuario("Ana")           # rol por defecto
registrar_usuario("Luis", rol="admin")  # rol personalizado

# =========================================================
# 5. Buenas prácticas
# =========================================================

# - Usa keyword arguments para mejorar legibilidad en funciones con muchos parámetros
# - Mantén consistencia en el orden: primero posicional, luego nombrado
# - Evita demasiados parámetros: si hay más de 4-5, considera agrupar en dict o dataclass
# - Documenta los parámetros en docstrings
