# atributos_instancia_vs_clase.py
# Estado compartido vs estado propio
# Orientado a backend y proyectos de datos

"""
En Python, los atributos pueden ser de instancia o de clase.
- Instancia: cada objeto tiene su propio valor.
- Clase: todos los objetos comparten el mismo valor.
Esto es clave para modelar datos correctamente en sistemas reales.
"""

# -------------------------------------------------
# 1. Atributos de instancia
# -------------------------------------------------
class Usuario:
    """
    Cada usuario tiene su propio nombre y email.
    Estos son atributos de instancia.
    """
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email

# Crear instancias
usuario1 = Usuario("Ana", "ana@email.com")
usuario2 = Usuario("Luis", "luis@email.com")

usuario1.nombre = "Ana María"
print(usuario1.nombre)  # Ana María
print(usuario2.nombre)  # Luis

# Observa: cada instancia mantiene su propio estado.

# -------------------------------------------------
# 2. Atributos de clase
# -------------------------------------------------
class Configuracion:
    """
    Todas las instancias comparten el mismo valor por defecto.
    Útil para constantes globales o valores compartidos.
    """
    version = "1.0"  # atributo de clase

config1 = Configuracion()
config2 = Configuracion()

print(config1.version)  # 1.0
print(config2.version)  # 1.0

# Cambiar el atributo de clase afecta a todas las instancias
Configuracion.version = "2.0"
print(config1.version)  # 2.0
print(config2.version)  # 2.0

# -------------------------------------------------
# 3. Mezcla de instancia y clase
# -------------------------------------------------
class Pedido:
    iva = 0.21  # atributo de clase, compartido por todos los pedidos

    def __init__(self, total_sin_iva: float):
        self.total_sin_iva = total_sin_iva  # atributo de instancia

    def total_con_iva(self) -> float:
        return self.total_sin_iva * (1 + Pedido.iva)

pedido1 = Pedido(100)
pedido2 = Pedido(200)

print(pedido1.total_con_iva())  # 121.0
print(pedido2.total_con_iva())  # 242.0

# Cambiamos el IVA para toda la clase
Pedido.iva = 0.10
print(pedido1.total_con_iva())  # 110.0
print(pedido2.total_con_iva())  # 220.0

# -------------------------------------------------
# 4. Buenas prácticas
# -------------------------------------------------
"""
1. Usa atributos de instancia para datos propios de cada objeto (ej: nombre, email, total de pedido).
2. Usa atributos de clase para valores compartidos entre todas las instancias (ej: versión, tasas, límites globales).
3. Evita modificar atributos de clase desde instancias directamente para no generar confusión.
4. En backend, atributos de clase son útiles para configurar valores globales que no cambian por usuario, pero la información individual siempre debe estar en atributos de instancia.
"""
