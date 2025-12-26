# eq_hash.py
# Cómo definir igualdad y hashing correctamente en Python, clave para sets, dicts y consistencia en backend

class Usuario:
    def __init__(self, usuario_id: int, nombre: str, email: str):
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.email = email

    def __eq__(self, other):
        # Igualdad basada en ID único del usuario
        if isinstance(other, Usuario):
            return self.usuario_id == other.usuario_id
        return False

    def __hash__(self):
        # Hash consistente con __eq__, necesario para usar en sets o dicts
        return hash(self.usuario_id)

    def __repr__(self):
        return f"Usuario({self.usuario_id}, {self.nombre!r}, {self.email!r})"

# ------------------------------------------------------------
# Uso en sets y diccionarios
usuarios_set = set()
u1 = Usuario(1, "Ana", "ana@example.com")
u2 = Usuario(1, "Ana Maria", "ana.maria@example.com")  # mismo ID, diferente nombre

usuarios_set.add(u1)
usuarios_set.add(u2)  # No se añade, porque __eq__ y __hash__ consideran que ya existe

print(usuarios_set)
# Output: {Usuario(1, 'Ana', 'ana@example.com')}

# Diccionarios usando objetos como claves
usuarios_dict = {u1: "activo"}
print(usuarios_dict[u2])  # Funciona porque u2 es considerado igual a u1
# Output: activo

# ------------------------------------------------------------
# CONSEJOS:
# 1. Siempre que sobrescribas __eq__, sobrescribe también __hash__ si quieres que el objeto sea hashable.
# 2. Define igualdad basada en identificadores únicos si el objeto representa una entidad real.
# 3. Esto evita bugs sutiles al usar objetos en sets o como claves de dicts.
# 4. Muy útil en backend para caches, colecciones de usuarios o recursos únicos.
