usuario = {
    "id": 123,
    "nombre": "Ana García",
    "email": "ana@empresa.com",
    "activo": True
}
# ✅ pop() con valor por defecto
departamento = usuario.pop("departamento", None)
print("Departamento eliminado:", departamento)  # None (no existía)

# ❌ pop() sin default → KeyError
# usuario.pop("direccion")  # ¡BOOM!

# ✅ del con chequeo
if "direccion" in usuario:
    del usuario["direccion"]

# ✅ popitem() (última clave-valor)
if usuario:
    ultimo = usuario.popitem()
    print("Último eliminado:", ultimo)
