# ejemplos_backend_basicos.py
# Modelos simples orientados a dominio en backend
# Orientado a tu caso: APIs y pipelines de datos

"""
En sistemas reales de backend o data engineering, modelamos entidades del dominio
con clases para encapsular datos y comportamiento relacionados.
Esto hace el código más legible, testable y mantenible.
"""

# -------------------------------------------------
# 1. Modelo de dominio básico: Usuario
# -------------------------------------------------
class Usuario:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email
        self.activo = True  # Estado inicial

    def desactivar(self):
        """Lógica de negocio: desactivar usuario"""
        self.activo = False

    def __repr__(self):
        return f"Usuario(nombre={self.nombre}, email={self.email}, activo={self.activo})"

# Crear instancias
usuario1 = Usuario("Ana", "ana@email.com")
usuario2 = Usuario("Luis", "luis@email.com")

usuario1.desactivar()
print(usuario1)  # Usuario(nombre=Ana, email=ana@email.com, activo=False)
print(usuario2)  # Usuario(nombre=Luis, email=luis@email.com, activo=True)

# -------------------------------------------------
# 2. Modelo de dominio con validación: Producto
# -------------------------------------------------
class Producto:
    def __init__(self, nombre: str, precio: float):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self.nombre = nombre
        self.precio = precio

    def aplicar_descuento(self, porcentaje: float):
        """Aplica descuento, validando que no sea negativo"""
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("Porcentaje inválido")
        self.precio *= (1 - porcentaje / 100)

    def __repr__(self):
        return f"Producto(nombre={self.nombre}, precio={self.precio:.2f})"

# Uso típico en backend
producto1 = Producto("Laptop", 1500.0)
producto1.aplicar_descuento(10)
print(producto1)  # Producto(nombre=Laptop, precio=1350.00)

# -------------------------------------------------
# 3. Modelo orientado a pipelines: DataBatch
# -------------------------------------------------
from typing import List, Dict

class DataBatch:
    """Representa un lote de datos en un pipeline"""
    def __init__(self, registros: List[Dict]):
        self.registros = registros

    def filtrar_por_campo(self, campo: str, valor):
        """Devuelve solo registros donde campo == valor"""
        return [r for r in self.registros if r.get(campo) == valor]

    def resumen(self):
        """Resumen rápido del batch"""
        return {
            "total": len(self.registros),
            "campos": list(self.registros[0].keys()) if self.registros else []
        }

# Ejemplo de uso
batch = DataBatch([
    {"id": 1, "nombre": "Ana", "edad": 30},
    {"id": 2, "nombre": "Luis", "edad": 25},
])
print(batch.filtrar_por_campo("edad", 25))  # [{'id': 2, 'nombre': 'Luis', 'edad': 25}]
print(batch.resumen())  # {'total': 2, 'campos': ['id', 'nombre', 'edad']}

# -------------------------------------------------
# 4. Buenas prácticas en modelos de backend
# -------------------------------------------------
"""
- Validaciones dentro del constructor o métodos para asegurar integridad de datos.
- Encapsular lógica relacionada dentro de la clase (desactivar usuario, aplicar descuento).
- Mantener modelos del dominio separados de la infraestructura (DB, API).
- Facilitar testabilidad y mantenimiento.
"""
