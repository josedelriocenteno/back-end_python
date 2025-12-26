# map_filter_zip_en_contexto.py
"""
Uso Profesional de map, filter y zip en Python

Este módulo cubre:
- Aplicación práctica de map, filter y zip
- Transformación y filtrado eficiente de datos
- Ejemplos orientados a backend y pipelines
"""

# -------------------------------------------------
# 1. map() – Transformar datos
# -------------------------------------------------
usuarios = ["juan", "pedro", "maria"]

# Tradicional
usuarios_mayus = []
for u in usuarios:
    usuarios_mayus.append(u.upper())

# Profesional con map
usuarios_mayus = list(map(str.upper, usuarios))
print(usuarios_mayus)  # ['JUAN','PEDRO','MARIA']

# -------------------------------------------------
# 2. filter() – Filtrar datos
# -------------------------------------------------
edades = [15, 22, 30, 18]

# Tradicional
mayores = []
for e in edades:
    if e >= 18:
        mayores.append(e)

# Profesional con filter
mayores = list(filter(lambda x: x >= 18, edades))
print(mayores)  # [22,30,18]

# -------------------------------------------------
# 3. zip() – Combinar listas
# -------------------------------------------------
usuarios = ["juan", "pedro", "maria"]
edades = [25, 30, 22]

# Tradicional
usuario_edad = []
for i in range(len(usuarios)):
    usuario_edad.append((usuarios[i], edades[i]))

# Profesional con zip
usuario_edad = list(zip(usuarios, edades))
print(usuario_edad)  # [('juan',25),('pedro',30),('maria',22)]

# -------------------------------------------------
# 4. Combinando map, filter y zip
# -------------------------------------------------
# Objetivo: nombres en mayúsculas de usuarios mayores de 22 años
usuario_edad_dict = dict(zip(usuarios, edades))
usuarios_filtrados = list(
    map(
        str.upper,
        filter(lambda u: usuario_edad_dict[u] > 22, usuario_edad_dict)
    )
)
print(usuarios_filtrados)  # ['PEDRO']

# -------------------------------------------------
# 5. Aplicación en backend y data pipelines
# -------------------------------------------------
# Filtrado y transformación de logs
logs = [
    "INFO | usuario juan creado",
    "ERROR | fallo DB",
    "INFO | usuario pedro creado"
]

# Extraer nombres de usuarios de logs INFO
nombres_info = list(
    map(
        lambda x: x.split()[2],
        filter(lambda x: x.startswith("INFO"), logs)
    )
)
print(nombres_info)  # ['juan','pedro']

# -------------------------------------------------
# 6. Errores comunes de juniors
# -------------------------------------------------
# ❌ No convertir map/filter a lista cuando se necesita
# ❌ Mezclar map y filter con bucles innecesarios
# ❌ Zip con listas de diferente longitud sin control
# ❌ Funciones lambda complejas dentro de map/filter → ilegible

# -------------------------------------------------
# 7. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Convertir map/filter a lista o iterar directamente si es iterador
# ✔️ Mantener lambdas simples o usar funciones nombradas
# ✔️ Usar zip solo con listas de igual longitud o manejar excepciones
# ✔️ Documentar transformaciones complejas
# ✔️ Combinar map/filter/zip para pipelines de datos concisos y eficientes

# -------------------------------------------------
# 8. Checklist mental backend
# -------------------------------------------------
# ✔️ Transformaciones y filtrado claros y concisos?  
# ✔️ Evitar loops innecesarios?  
# ✔️ Uso correcto de iteradores vs listas?  
# ✔️ Código mantenible y legible?

# -------------------------------------------------
# 9. Regla de oro
# -------------------------------------------------
"""
En backend profesional:
- map, filter y zip son herramientas esenciales para transformar, filtrar y combinar datos
- Úsalas de manera concisa, legible y eficiente
- Esto garantiza pipelines, APIs y procesamiento de datos robusto y profesional
"""
