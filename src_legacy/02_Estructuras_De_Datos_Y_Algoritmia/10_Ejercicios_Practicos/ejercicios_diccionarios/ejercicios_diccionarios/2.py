usuario = {
    "id": 123,
    "nombre": "Ana García",
    "email": "ana@empresa.com",
    "activo": True
}
# ✅ MÉTODO 1: get() con valor por defecto
telefono = usuario.get("telefono", "No proporcionado")
print("Teléfono:", telefono)  # No proporcionado

# ✅ MÉTODO 2: get() con None
edad = usuario.get("edad")
print("Edad:", edad)  # None

# ✅ MÉTODO 3: defaultdict
from collections import defaultdict
usuario_default = defaultdict(lambda: "Desconocido")
print(usuario_default["direccion"])  # Desconocido
