# que_es_poo_en_python.py
# Qué aporta la POO en sistemas reales

"""
La Programación Orientada a Objetos (POO) es un paradigma que organiza el código en 'objetos' que combinan
estado (atributos) y comportamiento (métodos). Permite modelar entidades reales de manera más clara y mantenible.

Ventajas principales:
1. Modularidad: Cada clase representa un componente independiente.
2. Reutilización: Herencia y composición permiten usar código existente sin duplicarlo.
3. Mantenibilidad: Cambios locales no afectan al resto si el código está bien encapsulado.
4. Escalabilidad: Facilita la incorporación de nuevas funcionalidades.
5. Testabilidad: Objetos con responsabilidades claras se pueden probar aisladamente.

Ejemplo práctico:
"""
class Usuario:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email
        self.rol = "usuario"  # atributo de instancia

    def saludar(self):
        return f"Hola, soy {self.nombre} y mi rol es {self.rol}"

# Uso
u1 = Usuario("Ana", "ana@example.com")
print(u1.saludar())  # Hola, soy Ana y mi rol es usuario

"""
Aplicación en sistemas reales:
- Modelar entidades de negocio: Usuario, Producto, Pedido.
- Control de acceso: métodos privados y públicos.
- Encapsular lógica: validaciones, cálculos, transformaciones.
- Facilita migración entre capas: Domain, Application, Infrastructure.
"""
