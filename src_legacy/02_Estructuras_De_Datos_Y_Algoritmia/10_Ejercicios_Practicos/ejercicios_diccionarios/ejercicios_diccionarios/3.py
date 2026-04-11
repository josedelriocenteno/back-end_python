usuario = {
    "id": 123,
    "nombre": "Ana García",
    "email": "ana@empresa.com",
    "activo": True
}
# ✅ update() con otro diccionario
actualizaciones = {
    "email": "ana.nueva@empresa.com",
    "telefono": "+34 123 456 789",
    "activo": False
}

usuario.update(actualizaciones)
print("Actualizado:", usuario)

# ✅ update() con lista de tuplas
usuario.update([("departamento", "IT"), ("salario", 45000)])
print("Más updates:", usuario)
