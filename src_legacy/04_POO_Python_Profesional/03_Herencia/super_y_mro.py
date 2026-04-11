# super_y_mro.py
# Ejemplo práctico de super() y Method Resolution Order (MRO) en Python
# Orientado a backend y diseño de clases profesionales

"""
En Python, super() permite acceder a métodos de la clase base.
El MRO (Method Resolution Order) define el orden en que Python busca
un método en la jerarquía de clases, especialmente útil en herencia múltiple.
"""

# -------------------------------------------------
# HERENCIA SIMPLE
# -------------------------------------------------
class Usuario:
    def saludar(self):
        print("Hola, soy un usuario")

class Administrador(Usuario):
    def saludar(self):
        print("Hola, soy un administrador")
        super().saludar()  # Llamada al método de la clase base

admin = Administrador()
admin.saludar()
# Salida:
# Hola, soy un administrador
# Hola, soy un usuario

# -------------------------------------------------
# HERENCIA MÚLTIPLE
# -------------------------------------------------
class Auditor:
    def saludar(self):
        print("Hola, soy un auditor")

class SuperUsuario(Administrador, Auditor):
    def saludar(self):
        print("Hola, soy un superusuario")
        super().saludar()  # super() sigue el MRO

super_user = SuperUsuario()
super_user.saludar()
# Salida:
# Hola, soy un superusuario
# Hola, soy un administrador
# Hola, soy un usuario

# -------------------------------------------------
# MRO EXPLICADO
# -------------------------------------------------
print(SuperUsuario.__mro__)
# Resultado: muestra el orden en que Python busca métodos:
# (<class '__main__.SuperUsuario'>, <class '__main__.Administrador'>,
# <class '__main__.Usuario'>, <class '__main__.Auditor'>, <class 'object'>)

# -------------------------------------------------
# Buenas prácticas
# -------------------------------------------------
"""
1. Usa super() siempre que quieras extender métodos de la clase base,
   especialmente __init__ y métodos críticos.
2. En herencia múltiple, revisa el MRO para evitar comportamientos inesperados.
3. Mantén jerarquías simples cuando sea posible para mayor claridad.
4. Evita depender de un orden de clases ambiguo: explícitamente define
   la herencia para que el MRO sea predecible.
"""
