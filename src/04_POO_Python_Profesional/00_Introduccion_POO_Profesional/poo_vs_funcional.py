# poo_vs_funcional.py
# Cuándo usar cada paradigma en Python
# Orientado a backend, data y proyectos reales

"""
En Python podemos combinar varios paradigmas: la programación orientada a objetos (POO) y la funcional (FP). 
Saber cuándo usar cada uno es clave para escribir código profesional, mantenible y eficiente.

Para tu caso: estás construyendo sistemas backend y pipelines de datos, donde tendrás:
- Entidades y modelos de dominio (POO)
- Transformaciones y procesamiento de datos (FP)
"""

# ---------------------------------------------
# 1. Programación Orientada a Objetos (POO)
# ---------------------------------------------
# POO modela el mundo real con objetos que tienen estado (atributos) y comportamiento (métodos). 
# Ideal para sistemas complejos, APIs y servicios donde necesitas encapsular datos y lógica.

# Ventajas de POO:
# - Encapsulamiento: protege datos y centraliza lógica.
# - Reutilización: herencia y composición permiten extender funcionalidades.
# - Claridad: cada entidad tiene responsabilidades claras.
# - Testabilidad: objetos bien diseñados permiten pruebas unitarias aisladas.

# Ejemplo práctico (backend de pedidos):
class Usuario:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email

    def saludar(self) -> str:
        return f"Hola, soy {self.nombre}"

class Pedido:
    def __init__(self, usuario: Usuario, productos: list[float]):
        self.usuario = usuario
        self.productos = productos

    def total(self) -> float:
        return sum(self.productos)

# Uso
usuario = Usuario("Ana", "ana@email.com")
pedido = Pedido(usuario, [10, 20, 30])
print(usuario.saludar())  # Hola, soy Ana
print(pedido.total())     # 60

# ---------------------------------------------
# 2. Programación Funcional (FP)
# ---------------------------------------------
# FP se centra en funciones puras que reciben datos y devuelven resultados sin modificar el estado externo.
# Perfecto para pipelines, ETL, transformaciones y cálculos puros.

# Ventajas de FP:
# - Composición fácil de funciones
# - Reduce efectos secundarios
# - Ideal para manipular colecciones grandes y hacer cálculos deterministas

productos = [10, 20, 30]

# Función pura
def calcular_total(lista: list[float]) -> float:
    return sum(lista)

total = calcular_total(productos)
print(total)  # 60

# Pipeline funcional con map y filter
precios_descuento = list(map(lambda x: x*0.9, productos))
precios_filtrados = list(filter(lambda x: x >= 15, precios_descuento))
print(precios_filtrados)  # [18.0, 27.0]

# ---------------------------------------------
# 3. Cuándo usar cada paradigma
# ---------------------------------------------
# - POO: sistemas complejos, backend, APIs, entidades con relaciones, lógica de negocio.
# - Funcional: procesamiento de datos, pipelines, transformaciones masivas, cálculos deterministas.
# - Híbrido: Python permite mezclar ambos. Por ejemplo, modela entidades con POO y usa FP dentro de métodos para cálculos o filtrados.

# Ejemplo híbrido realista
class PedidoHibrido:
    def __init__(self, productos: list[float]):
        self.productos = productos

    def total_con_descuento(self) -> float:
        # Función pura dentro de un método
        aplicar_descuento = lambda lista: sum(map(lambda x: x*0.9, lista))
        return aplicar_descuento(self.productos)

productos_raw = [10, 20, 30]
pedido_hibrido = PedidoHibrido(productos_raw)
print(pedido_hibrido.total_con_descuento())  # 54.0

# ---------------------------------------------
# 4. Consejos prácticos para backend y pipelines
# ---------------------------------------------
# 1. Modela entidades, repositorios y servicios con POO
# 2. Usa funciones puras para cálculos, filtros y transformaciones de datos
# 3. Evita clases “anémicas” que solo guardan datos; combina comportamiento y estado
# 4. Aplica FP dentro de métodos de clase para operaciones internas sin efectos secundarios
# 5. Piensa siempre en testabilidad y mantenibilidad: FP facilita tests unitarios, POO organiza la arquitectura
