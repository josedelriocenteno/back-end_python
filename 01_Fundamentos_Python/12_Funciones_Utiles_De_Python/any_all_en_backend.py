# any_all_en_backend.py
"""
Uso Profesional de any() y all() en Backend

Este módulo cubre:
- Validaciones y comprobaciones de condiciones
- Aplicación en pipelines de datos y backend
- Ejemplos prácticos y buenas prácticas profesionales
"""

# -------------------------------------------------
# 1. any() – Al menos una condición verdadera
# -------------------------------------------------
edades = [15, 22, 30, 18]

# ¿Hay algún menor de edad?
hay_menor = any(e < 18 for e in edades)
print(hay_menor)  # True

# Aplicación backend: bloquear acceso si algún dato es inválido
inputs = ["juan@example.com", "", "pedro@example.com"]
hay_vacio = any(i == "" for i in inputs)
if hay_vacio:
    print("Error: campos vacíos encontrados!")

# -------------------------------------------------
# 2. all() – Todas las condiciones verdaderas
# -------------------------------------------------
# ¿Todos son adultos?
todos_mayores = all(e >= 18 for e in edades)
print(todos_mayores)  # False

# Validación de datos en pipelines
emails = ["juan@example.com", "pedro@example.com"]
validos = all("@" in email for email in emails)
print(validos)  # True

# -------------------------------------------------
# 3. Combinando any() y all()
# -------------------------------------------------
usuarios = [{"nombre":"juan","edad":25},{"nombre":"pedro","edad":17}]
# ¿Todos mayores de 18 y al menos uno tiene nombre 'juan'?
condicion = all(u["edad"] >= 18 for u in usuarios) and any(u["nombre"]=="juan" for u in usuarios)
print(condicion)  # False

# -------------------------------------------------
# 4. Uso en listas y comprehensions
# -------------------------------------------------
numeros = [2,4,6,8]
# ¿Todos pares y alguno mayor que 5?
resultado = all(n % 2 == 0 for n in numeros) and any(n > 5 for n in numeros)
print(resultado)  # True

# -------------------------------------------------
# 5. Errores comunes de juniors
# -------------------------------------------------
# ❌ Confundir any() con all()
# ❌ No usar generadores → crear listas innecesarias
# ❌ Condiciones demasiado complejas dentro de any/all → ilegible
# ❌ Olvidar casos vacíos (any([]) = False, all([]) = True)

# -------------------------------------------------
# 6. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Usar generadores en vez de listas cuando sea posible: ahorro de memoria
# ✔️ Mantener condiciones claras y simples
# ✔️ Documentar validaciones críticas
# ✔️ Combinar any/all para checks complejos de manera legible
# ✔️ Testear todos los casos límite, incluyendo listas vacías

# -------------------------------------------------
# 7. Checklist mental backend
# -------------------------------------------------
# ✔️ Validaciones claras y concisas?  
# ✔️ Generadores usados en lugar de listas cuando es posible?  
# ✔️ Código legible y mantenible?  
# ✔️ Condiciones críticas correctamente validadas?

# -------------------------------------------------
# 8. Regla de oro
# -------------------------------------------------
"""
En backend profesional:
- any() = al menos una condición verdadera
- all() = todas las condiciones verdaderas
- Generadores = eficiencia en memoria
- Esto garantiza validaciones robustas y pipelines de datos confiables
"""
