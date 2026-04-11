# ocp_open_closed.py

"""
Open/Closed Principle (OCP)
---------------------------
Las entidades de software (clases, módulos, funciones) deben estar:
- ABIERTAS para extensión
- CERRADAS para modificación

Es decir:
👉 deberías poder añadir nuevo comportamiento SIN tocar el código existente.

Esto es CRÍTICO en backend y sistemas reales:
- Evita romper código en producción
- Reduce bugs colaterales
- Permite escalar lógica de negocio sin reescribirlo todo

Si cada nuevo requisito te obliga a modificar 5 clases existentes,
NO estás aplicando OCP.
"""

# ============================================================
# ❌ MAL EJEMPLO: violación del OCP
# ============================================================

class CalculadoraEnvio:
    def calcular(self, tipo_envio: str, peso: float) -> float:
        if tipo_envio == "normal":
            return peso * 1.0
        elif tipo_envio == "express":
            return peso * 2.0
        elif tipo_envio == "internacional":
            return peso * 5.0
        else:
            raise ValueError("Tipo de envío no soportado")

"""
PROBLEMA REAL:
- Cada nuevo tipo de envío → modificar esta clase
- Riesgo de romper lógica existente
- if/elif infinitos
- Muy difícil de testear correctamente

Esto es código de estudiante, no de backend profesional.
"""

# ============================================================
# ✅ BUEN EJEMPLO: aplicando OCP con polimorfismo
# ============================================================

from abc import ABC, abstractmethod


class Envio(ABC):
    """
    Abstracción.
    Define el CONTRATO, no la implementación.
    """
    @abstractmethod
    def calcular_coste(self, peso: float) -> float:
        pass


class EnvioNormal(Envio):
    def calcular_coste(self, peso: float) -> float:
        return peso * 1.0


class EnvioExpress(Envio):
    def calcular_coste(self, peso: float) -> float:
        return peso * 2.0


class EnvioInternacional(Envio):
    def calcular_coste(self, peso: float) -> float:
        return peso * 5.0


class CalculadoraEnvio:
    """
    Esta clase ya NO CAMBIA.
    Está cerrada a modificación.
    """
    def calcular(self, envio: Envio, peso: float) -> float:
        return envio.calcular_coste(peso)


# ============================================================
# USO REAL (backend / servicios)
# ============================================================

if __name__ == "__main__":
    calculadora = CalculadoraEnvio()

    envio_normal = EnvioNormal()
    envio_express = EnvioExpress()

    print(calculadora.calcular(envio_normal, 10))
    print(calculadora.calcular(envio_express, 10))

"""
¿Quieres añadir un nuevo tipo de envío?
- NO tocas CalculadoraEnvio
- NO rompes código existente
- SOLO añades una nueva clase
"""


# ============================================================
# 🔥 EXTENSIÓN REAL SIN MODIFICAR NADA
# ============================================================

class EnvioSameDay(Envio):
    def calcular_coste(self, peso: float) -> float:
        return peso * 3.5


envio_same_day = EnvioSameDay()
print(calculadora.calcular(envio_same_day, 10))

"""
Esto es OCP bien aplicado.
"""


# ============================================================
# 💡 POR QUÉ ESTO ES CLAVE PARA TU CASO (backend + data)
# ============================================================

"""
En tu camino hacia backend e IA:

✔ APIs que crecen con nuevos comportamientos
✔ Pipelines de datos con nuevas transformaciones
✔ Sistemas que viven años en producción

OCP te permite:
- Añadir features sin miedo
- Versionar lógica fácilmente
- Mantener código limpio y testeable
- Pensar en extensiones, no parches

Regla mental:
❗ Si añades un if nuevo para soportar un caso → revisa tu diseño.
"""

