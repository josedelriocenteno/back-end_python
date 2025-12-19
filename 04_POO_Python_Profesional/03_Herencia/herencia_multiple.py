# herencia_multiple.py
# Ejemplo de uso controlado de herencia múltiple en Python
# Orientado a backend profesional y diseño de clases robustas

"""
La herencia múltiple permite que una clase herede de varias clases base.
Es potente, pero puede ser peligrosa si no se controla: puede generar
confusión con el MRO, conflictos de métodos o acoplamiento fuerte.
"""

# -------------------------------------------------
# CLASES BASE
# -------------------------------------------------
class Logger:
    def log(self, mensaje):
        print(f"[LOG] {mensaje}")

class ConectorBaseDatos:
    def conectar(self):
        print("Conectando a la base de datos...")

# -------------------------------------------------
# HERENCIA MÚLTIPLE
# -------------------------------------------------
class Servicio(Logger, ConectorBaseDatos):
    def ejecutar(self):
        self.log("Inicio de ejecución")
        self.conectar()
        self.log("Fin de ejecución")

servicio = Servicio()
servicio.ejecutar()
# Salida:
# [LOG] Inicio de ejecución
# Conectando a la base de datos...
# [LOG] Fin de ejecución

# -------------------------------------------------
# POSIBLES PELIGROS
# -------------------------------------------------
class Auditor:
    def log(self, mensaje):
        print(f"[AUDITOR] {mensaje}")

# Clase que hereda de Logger y Auditor puede generar conflictos de métodos
class ServicioConfuso(Logger, Auditor):
    def ejecutar(self):
        self.log("Ejecución conflictiva")

confuso = ServicioConfuso()
confuso.ejecutar()
# Salida:
# [LOG] Ejecución conflictiva
# Python usa MRO: Logger.log se ejecuta antes que Auditor.log

# -------------------------------------------------
# BUENAS PRÁCTICAS
# -------------------------------------------------
"""
1. Evita herencia múltiple si no es estrictamente necesario.
2. Si la usas, asegúrate de entender el MRO y cómo se resuelven los métodos.
3. Considera la composición sobre la herencia múltiple: 
   crea objetos internos en lugar de mezclar jerarquías complejas.
4. Documenta claramente qué clases base estás combinando y por qué.
"""
