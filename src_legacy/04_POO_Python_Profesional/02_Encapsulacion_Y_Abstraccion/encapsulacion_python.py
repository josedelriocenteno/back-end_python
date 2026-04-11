# encapsulacion_python.py
# Ejemplo de encapsulación en Python
# Orientado a tu caso: backend y pipelines de datos

"""
La encapsulación permite controlar el acceso a los atributos y métodos
de una clase, protegiendo el estado interno y evitando modificaciones
accidentales desde fuera de la clase.

En Python, usamos:
- _atributo: convención de uso protegido (para uso interno)
- __atributo: name mangling, no accesible directamente desde fuera
"""

# -------------------------------------------------
# Clase con atributos protegidos y privados
# -------------------------------------------------
class CuentaBancaria:
    def __init__(self, titular: str, saldo: float):
        self.titular = titular          # público
        self._saldo = saldo             # protegido, convención interna
        self.__pin = "1234"             # privado (name mangling)

    # Método público para acceder al saldo de manera segura
    def mostrar_saldo(self, pin: str):
        if pin == self.__pin:
            return self._saldo
        else:
            raise ValueError("PIN incorrecto")

    # Método protegido para actualizar saldo internamente
    def _modificar_saldo(self, cantidad: float):
        self._saldo += cantidad

    # Método privado para validaciones internas
    def __validar_transaccion(self, cantidad: float):
        if cantidad < 0 and abs(cantidad) > self._saldo:
            raise ValueError("Fondos insuficientes")

# -------------------------------------------------
# Uso de la clase
# -------------------------------------------------
cuenta = CuentaBancaria("Ana", 1000.0)

# Acceso público
print(cuenta.titular)              # Ana
print(cuenta.mostrar_saldo("1234"))  # 1000.0

# Acceso protegido (convención, posible pero no recomendable)
cuenta._modificar_saldo(200)
print(cuenta.mostrar_saldo("1234"))  # 1200.0

# Acceso privado directo falla
try:
    print(cuenta.__pin)
except AttributeError:
    print("No se puede acceder a __pin directamente")

# Pero podemos ver cómo Python hace name mangling
print(cuenta._CuentaBancaria__pin)  # 1234 (solo para debug, no usar en producción)

# -------------------------------------------------
# Buenas prácticas
# -------------------------------------------------
"""
1. Usa atributos privados solo cuando sea necesario proteger datos críticos.
2. Los métodos y atributos con _ son para uso interno; respeta la convención.
3. Encapsula validaciones y lógica crítica dentro de la clase.
4. Facilita testeo mediante métodos públicos que usan internamente atributos protegidos o privados.
"""
