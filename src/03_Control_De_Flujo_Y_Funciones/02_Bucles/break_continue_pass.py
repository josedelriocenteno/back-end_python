# break_continue_pass.py
"""
CONTROL FINO DE FLUJO EN BUCLES
===============================

Objetivo:
- Aprender a usar break, continue y pass correctamente
- Mejorar legibilidad y eficiencia de bucles
- Aplicable a backend, pipelines de datos y scripts profesionales
"""

# =========================================================
# 1. BREAK
# =========================================================

numeros = [1, 2, 3, 4, 5]

for n in numeros:
    if n == 3:
        print("Encontrado 3, saliendo del bucle")
        break  # Sale inmediatamente del bucle
    print(n)

# =========================================================
# 2. CONTINUE
# =========================================================

for n in numeros:
    if n % 2 == 0:
        print(f"Omitiendo número par: {n}")
        continue  # Salta a la siguiente iteración
    print(f"Número impar: {n}")

# =========================================================
# 3. PASS
# =========================================================

for n in numeros:
    if n == 3:
        pass  # Placeholder: se puede implementar más tarde
    print(f"Procesando: {n}")

# =========================================================
# 4. Buenas prácticas
# =========================================================

# - Usar break para salir temprano cuando la condición principal se cumple
# - Usar continue para saltar casos excepcionales o no relevantes
# - Usar pass solo como marcador temporal, no como lógica final
# - Evitar lógica compleja mezclada en el cuerpo del bucle

# =========================================================
# 5. Aplicación profesional
# =========================================================

# Backend/data: procesamiento de listas, filtrado de datos, búsqueda eficiente
usuarios = [
    {"nombre": "Ana", "edad": 25},
    {"nombre": "Luis", "edad": 17},
    {"nombre": "Marta", "edad": 30}
]

for usuario in usuarios:
    if usuario["edad"] < 18:
        continue  # Saltar menores
    if usuario["nombre"] == "Marta":
        print("Usuario Marta encontrado, terminando bucle")
        break  # Terminar procesamiento
    print(f"Procesando usuario: {usuario['nombre']}")
