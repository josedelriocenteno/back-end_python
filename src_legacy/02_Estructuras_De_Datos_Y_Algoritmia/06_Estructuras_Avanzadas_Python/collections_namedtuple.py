# collections_namedtuple.py
"""
COLLECTIONS.NAMEDTUPLE EN PYTHON — ALTERNATIVA LIGERA A CLASES
===============================================================

Objetivo:
- Usar namedtuple para crear estructuras de datos inmutables y legibles
- Evitar boilerplate de clases simples
- Aplicaciones en backend, pipelines y procesamiento de datos
"""

from collections import namedtuple

# ------------------------------------------------------------
# 1. CREACIÓN DE UN NAMEDTUPLE
# ------------------------------------------------------------

# Definir un tipo de dato
Persona = namedtuple("Persona", ["nombre", "edad", "email"])

# Crear instancias
p1 = Persona(nombre="Alice", edad=30, email="alice@example.com")
p2 = Persona(nombre="Bob", edad=25, email="bob@example.com")

print("Persona 1:", p1)
print("Persona 2:", p2)

# Acceso por campo
print("Nombre de p1:", p1.nombre)
print("Edad de p2:", p2.edad)


# ------------------------------------------------------------
# 2. INMUTABILIDAD
# ------------------------------------------------------------

# Los namedtuple son inmutables
try:
    p1.edad = 31
except AttributeError as e:
    print("Error de inmutabilidad:", e)


# ------------------------------------------------------------
# 3. MÉTODOS ÚTILES
# ------------------------------------------------------------

# _fields → lista de campos
print("Campos de Persona:", Persona._fields)

# _replace → crea nueva instancia con cambios
p1_nuevo = p1._replace(edad=31)
print("p1 actualizado con _replace:", p1_nuevo)

# _asdict → convertir a diccionario
print("p1 como dict:", p1._asdict())


# ------------------------------------------------------------
# 4. USOS COMUNES EN BACKEND / DATA
# ------------------------------------------------------------

"""
- Representar filas de datos con nombres de columnas
- Devolver objetos desde funciones de forma legible
- Pipelines de procesamiento: mantener inmutabilidad
- Logs y reportes estructurados
"""

# Ejemplo: fila de pipeline
Fila = namedtuple("Fila", ["id", "valor", "timestamp"])
fila1 = Fila(1, 42.5, "2025-12-19 10:00")
print("Fila de pipeline:", fila1)


# ------------------------------------------------------------
# 5. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Modificar campos directamente → AttributeError
❌ Usar dicts simples en vez de namedtuple cuando necesitas acceso por atributo
❌ Confundir _replace con asignación
"""

# ✔ Correcto
fila2 = fila1._replace(valor=50)
print("Fila actualizada:", fila2)


# ------------------------------------------------------------
# 6. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Usa namedtuple para datos inmutables simples
✔ Documenta campos y tipos
✔ Prefiere _replace para cambios, no modificar campos
✔ Convierte a dict si necesitas serializar
✔ Evita crear clases completas si solo necesitas contenedor ligero
"""

print("collections.namedtuple dominado profesionalmente")
