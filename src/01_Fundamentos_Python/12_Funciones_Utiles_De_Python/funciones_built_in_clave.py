# funciones_built_in_clave.py
"""
Funciones Built-in Clave en Python – Backend Profesional

Este módulo cubre:
- Funciones built-in esenciales
- Transformación, filtrado, búsqueda y agregación de datos
- Buenas prácticas para backend y data pipelines
"""

# -------------------------------------------------
# 1. map()
# -------------------------------------------------
numeros = [1, 2, 3, 4, 5]

# Tradicional
cuadrados = []
for n in numeros:
    cuadrados.append(n**2)

# Con map
cuadrados_map = list(map(lambda x: x**2, numeros))
print(cuadrados_map)  # [1,4,9,16,25]

# -------------------------------------------------
# 2. filter()
# -------------------------------------------------
# Filtrar números pares
pares = list(filter(lambda x: x % 2 == 0, numeros))
print(pares)  # [2,4]

# -------------------------------------------------
# 3. zip()
# -------------------------------------------------
usuarios = ["juan", "pedro", "maria"]
edades = [25, 30, 22]

# Combinar listas
combinado = list(zip(usuarios, edades))
print(combinado)  # [('juan',25),('pedro',30),('maria',22)]

# Útil para dict comprehensions
usuarios_dict = {u: e for u, e in zip(usuarios, edades)}
print(usuarios_dict)

# -------------------------------------------------
# 4. enumerate()
# -------------------------------------------------
# Iterar con índice
for i, valor in enumerate(usuarios):
    print(i, valor)

# -------------------------------------------------
# 5. any() y all()
# -------------------------------------------------
numeros_mixtos = [2, 4, 6, 8]
print(all(n % 2 == 0 for n in numeros_mixtos))  # True
print(any(n > 5 for n in numeros_mixtos))       # True

# -------------------------------------------------
# 6. sorted() y reversed()
# -------------------------------------------------
lista = [5, 2, 9, 1]
print(sorted(lista))       # [1,2,5,9]
print(sorted(lista, reverse=True))  # [9,5,2,1]
print(list(reversed(lista)))       # [1,9,2,5] (no ordena, invierte)

# -------------------------------------------------
# 7. sum(), min(), max()
# -------------------------------------------------
print(sum(numeros))  # 15
print(min(numeros))  # 1
print(max(numeros))  # 5

# -------------------------------------------------
# 8. type(), isinstance()
# -------------------------------------------------
print(type(numeros))           # <class 'list'>
print(isinstance(numeros, list))  # True

# -------------------------------------------------
# 9. str(), int(), float()
# -------------------------------------------------
print(int("123"))    # 123
print(str(123))      # '123'
print(float("12.34")) # 12.34

# -------------------------------------------------
# 10. Errores comunes de juniors
# -------------------------------------------------
# ❌ No usar built-ins y hacer loops largos innecesarios
# ❌ Confundir any() con all()
# ❌ Usar zip() sin desempaquetar correctamente
# ❌ Usar map/filter sin convertir a lista cuando se necesita
# ❌ Ignorar tipo de datos y casting

# -------------------------------------------------
# 11. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Usar built-ins siempre que sean claros y eficientes
# ✔️ Preferir comprehensions combinadas con any/all/map/filter
# ✔️ Documentar transformaciones complejas
# ✔️ Validar tipos antes de operar
# ✔️ Evitar loops innecesarios

# -------------------------------------------------
# 12. Checklist mental backend
# -------------------------------------------------
# ✔️ Se usan built-ins correctamente?  
# ✔️ Código más conciso y eficiente?  
# ✔️ Transformaciones claras y reproducibles?  
# ✔️ Evitando bucles innecesarios?

# -------------------------------------------------
# 13. Regla de oro
# -------------------------------------------------
"""
En backend profesional:
- Dominar built-ins = código más limpio, eficiente y mantenible
- Transformaciones de datos claras y concisas
- Esto garantiza pipelines, APIs y lógica de negocio robusta y profesional
"""
