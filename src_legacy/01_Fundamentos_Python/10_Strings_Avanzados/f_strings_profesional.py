# f_strings_profesional.py
"""
f-Strings Profesionales en Python – Nivel Backend Profesional

Este módulo cubre:
- Uso de f-strings para formateo
- Expresiones dentro de f-strings
- Formateo avanzado (números, fechas, padding)
- Buenas prácticas profesionales
"""

from datetime import datetime

# -------------------------------------------------
# 1. Formateo básico
# -------------------------------------------------
nombre = "Juan"
edad = 25

# f-string simple
mensaje = f"Usuario: {nombre}, Edad: {edad}"
print(mensaje)

# Equivalente usando format() (menos claro)
mensaje2 = "Usuario: {}, Edad: {}".format(nombre, edad)

# -------------------------------------------------
# 2. Expresiones dentro de f-strings
# -------------------------------------------------
print(f"Siguiente año: {edad + 1}")
print(f"Nombre en mayúsculas: {nombre.upper()}")

# -------------------------------------------------
# 3. Formateo de números
# -------------------------------------------------
precio = 1234.5678

# 2 decimales
print(f"Precio: {precio:.2f}")

# Separador de miles
print(f"Precio: {precio:,.2f}")

# Padding y alineación
print(f"|{nombre:<10}|{edad:^5}|")  # izquierda, centrado
print(f"|{nombre:>10}|{edad:>5}|")  # derecha

# -------------------------------------------------
# 4. Fechas y tiempo
# -------------------------------------------------
hoy = datetime.now()
print(f"Hoy es {hoy:%Y-%m-%d %H:%M:%S}")

# -------------------------------------------------
# 5. Formateo profesional en backend
# -------------------------------------------------
usuario = {
    "nombre": "juan.perez",
    "email": "juan.perez@example.com",
    "edad": 25,
}

log = f"{datetime.now():%Y-%m-%d %H:%M:%S} | INFO | Usuario {usuario['nombre']} ({usuario['email']}) registrado, Edad: {usuario['edad']}"
print(log)

# -------------------------------------------------
# 6. Errores comunes de juniors
# -------------------------------------------------
# ❌ Usar concatenación con + → menos legible y propenso a errores
# ❌ No usar padding ni alineación → logs confusos
# ❌ Olvidar redondear floats → salida inconsistente
# ❌ Ignorar expresiones → hacer operaciones fuera del f-string innecesariamente

# -------------------------------------------------
# 7. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Usar f-strings siempre que sea posible
# ✔️ Mantener expresiones claras y simples
# ✔️ Formatear números y fechas para legibilidad
# ✔️ Añadir padding/alineación en logs o tablas
# ✔️ Evitar concatenación clásica
# ✔️ Documentar transformaciones complejas

# -------------------------------------------------
# 8. Checklist mental backend
# -------------------------------------------------
# ✔️ Strings dinámicos claros y legibles?  
# ✔️ Expresiones dentro de f-strings controladas?  
# ✔️ Fechas y números formateados profesionalmente?  
# ✔️ Código robusto y mantenible?

# -------------------------------------------------
# 9. Regla de oro
# -------------------------------------------------
"""
En backend profesional:
- f-strings = claridad + eficiencia + seguridad
- Usar siempre padding y formateo cuando sea relevante
- Mantener logs y mensajes consistentes
- Esto garantiza un backend limpio, legible y profesional.
"""
