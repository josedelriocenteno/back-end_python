# composicion_basica.py
# Diferencia entre "tiene un" (composición) vs "es un" (herencia)
# Orientado a backend profesional y arquitectura escalable

"""
En desarrollo backend, la composición suele ser más flexible que la herencia.
- 'Es un': se usa cuando hay una relación de tipo, clara y estable.
- 'Tiene un': se usa para delegar responsabilidades, evitando jerarquías rígidas.
"""

# -------------------------------------------------
# EJEMPLO HERENCIA ("es un")
# -------------------------------------------------
class Vehiculo:
    def arrancar(self):
        print("Vehículo arrancado")

class Coche(Vehiculo):  # Coche 'es un' Vehiculo
    def abrir_maletero(self):
        print("Maletero abierto")

mi_coche = Coche()
mi_coche.arrancar()       # Vehículo arrancado
mi_coche.abrir_maletero() # Maletero abierto

# Problema: si Vehiculo cambia, puede romper Coche.
# Escalabilidad limitada.

# -------------------------------------------------
# EJEMPLO COMPOSICIÓN ("tiene un")
# -------------------------------------------------
class Motor:
    def arrancar(self):
        print("Motor arrancado")

class Auto:
    def __init__(self):
        self.motor = Motor()  # Auto 'tiene un' Motor

    def encender(self):
        self.motor.arrancar()
        print("Auto listo para conducir")

mi_auto = Auto()
mi_auto.encender()
# Salida:
# Motor arrancado
# Auto listo para conducir

# -------------------------------------------------
# LECCIONES
# -------------------------------------------------
"""
- Prefiere composición cuando quieres flexibilidad y evitar jerarquías frágiles.
- Composición permite cambiar partes internas sin afectar la interfaz externa.
- Herencia solo si hay una relación clara y estable "es un".
- En backend: servicios, repositorios y clientes suelen beneficiarse de composición.
"""
