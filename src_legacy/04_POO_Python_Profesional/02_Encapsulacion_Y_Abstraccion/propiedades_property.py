# propiedades_property.py
# Ejemplo de uso de @property y setters con validaciones
# Orientado a tu caso: backend, pipelines y entidades de datos

"""
@property permite exponer atributos como si fueran públicos,
pero controlando su acceso y agregando validaciones.
Esto mejora la seguridad y la mantenibilidad de tu código.
"""

# -------------------------------------------------
# Clase con property y setter
# -------------------------------------------------
class Producto:
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self._precio = 0.0
        self.precio = precio  # usa el setter para validar

    # Getter usando @property
    @property
    def precio(self):
        return self._precio

    # Setter con validación
    @precio.setter
    def precio(self, valor: float):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = valor

# -------------------------------------------------
# Uso de la clase
# -------------------------------------------------
producto = Producto("Teclado mecánico", 100.0)
print(producto.nombre)   # Teclado mecánico
print(producto.precio)   # 100.0

# Modificación usando setter
producto.precio = 120.0
print(producto.precio)   # 120.0

# Intento de asignación inválida
try:
    producto.precio = -50
except ValueError as e:
    print(e)  # El precio no puede ser negativo

# -------------------------------------------------
# Buenas prácticas
# -------------------------------------------------
"""
1. Usa @property cuando quieras exponer atributos públicos pero con control.
2. Valida dentro de setters para proteger el estado interno.
3. Evita exponer atributos internos directamente (usa _nombre).
4. Facilita la refactorización: puedes cambiar la implementación
   interna sin afectar el código que usa la clase.
5. Ideal para entidades de dominio, DTOs, modelos de datos y servicios.
"""
