# errores_herencia.py
# Ejemplo de jerarquías rígidas y frágiles en POO
# Orientado a tu caso: backend profesional y escalabilidad

"""
Los errores más comunes en herencia incluyen:
1. Jerarquías demasiado profundas.
2. Clases base que cambian y rompen todas las derivadas.
3. Herencia usada como atajo en lugar de composición.
4. Métodos sobreescritos sin respetar contrato o MRO.
"""

# -------------------------------------------------
# EJEMPLO DE JERARQUÍA RÍGIDA
# -------------------------------------------------
class Animal:
    def hablar(self):
        return "Sonido genérico"

class Perro(Animal):
    def hablar(self):
        return "Guau"

class PerroGrande(Perro):
    def hablar(self):
        return "GUAU GUAU"

# Problema: agregar un cambio en Animal puede romper toda la jerarquía
animal = Animal()
perro = Perro()
perro_grande = PerroGrande()

print(animal.hablar())        # Sonido genérico
print(perro.hablar())         # Guau
print(perro_grande.hablar())  # GUAU GUAU

# Si modificamos Animal.hablar(), todos los descendientes cambian comportamiento
# Esto demuestra fragilidad de la jerarquía.

# -------------------------------------------------
# MAL USO DE HERENCIA COMO ATJO
# -------------------------------------------------
class Usuario:
    def login(self):
        print("Login usuario")

class Admin(Usuario):
    def borrar_base_datos(self):
        print("Base de datos borrada!")

# Problema: Admin "hereda" de Usuario pero quizás solo necesitaba composición.
# Mejor: Admin tiene un objeto Usuario dentro y delega login.

# -------------------------------------------------
# LECCIÓN
# -------------------------------------------------
"""
- Evita jerarquías profundas, favorece la composición.
- Respeta el principio LSP (Liskov): cualquier subclase debe poder reemplazar a su base.
- Documenta y controla cambios en clases base.
- Usa herencia solo cuando haya una relación clara "es un".
"""
