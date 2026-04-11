# abc_basico.py
# Introducción a Abstract Base Classes (ABC) en Python
# Aplicado a un caso real: sistema de pagos en un backend de ecommerce

from abc import ABC, abstractmethod

class MetodoPago(ABC):
    """
    Clase abstracta que define la interfaz común para todos los métodos de pago.
    Garantiza que cualquier método implementará los métodos esenciales.
    """

    @abstractmethod
    def pagar(self, monto: float) -> bool:
        """
        Método obligatorio para procesar un pago.
        Debe retornar True si el pago fue exitoso, False en caso contrario.
        """
        pass

    @abstractmethod
    def obtener_detalles(self) -> dict:
        """
        Método obligatorio que retorna un resumen del método de pago.
        """
        pass

# ------------------------------------------------------------
# Implementaciones concretas

class TarjetaCredito(MetodoPago):
    def __init__(self, numero: str, titular: str, cvv: str):
        self.numero = numero
        self.titular = titular
        self.cvv = cvv

    def pagar(self, monto: float) -> bool:
        # Lógica simulada de pago con tarjeta
        print(f"Procesando pago de {monto}€ con tarjeta {self.numero[-4:]}")
        return True

    def obtener_detalles(self) -> dict:
        return {"tipo": "TarjetaCredito", "titular": self.titular, "ultimo_digito": self.numero[-4:]}

class PayPal(MetodoPago):
    def __init__(self, email: str):
        self.email = email

    def pagar(self, monto: float) -> bool:
        # Lógica simulada de pago con PayPal
        print(f"Procesando pago de {monto}€ con PayPal {self.email}")
        return True

    def obtener_detalles(self) -> dict:
        return {"tipo": "PayPal", "email": self.email}

# ------------------------------------------------------------
# Uso práctico

def procesar_pago(metodo: MetodoPago, monto: float):
    """
    Función que recibe cualquier implementación de MetodoPago.
    Gracias a ABC, garantizamos que los métodos necesarios existen.
    """
    if metodo.pagar(monto):
        print("Pago realizado con éxito")
    else:
        print("Error al procesar el pago")

# Probando los métodos concretos
tarjeta = TarjetaCredito("1234567812345678", "Juan Pérez", "123")
paypal = PayPal("juan@example.com")

procesar_pago(tarjeta, 150.0)
procesar_pago(paypal, 75.0)

# ------------------------------------------------------------
# CONCEPTOS CLAVE:
# 1. ABC garantiza que las subclases implementen los métodos esenciales.
# 2. Facilita polimorfismo: cualquier función puede recibir un MetodoPago.
# 3. Mejora mantenibilidad y diseño profesional en backend.
