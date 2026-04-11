# diseno_para_tests.py

"""
DISEÑO PARA TESTS EN PYTHON
===========================

Objetivo:
---------
Diseñar clases y funciones de manera que sean fáciles de probar,
facilitando la creación de tests unitarios y de integración sin depender
de implementaciones concretas de otras capas o servicios.

Buenas prácticas aplicadas a tu caso:
-------------------------------------
1. Separar lógica de negocio de persistencia o I/O.
2. Inyectar dependencias en lugar de crearlas internamente.
3. Evitar efectos secundarios en el constructor.
4. Usar clases pequeñas y enfocadas (Single Responsibility Principle).
"""

# ============================================================
# Ejemplo: clase fácil de testear
# ============================================================

from typing import List

class CalculadoraPromedios:
    """
    Clase simple que calcula promedios de listas de números.
    Sin dependencias externas, fácil de testear.
    """
    def calcular_promedio(self, numeros: List[float]) -> float:
        if not numeros:
            raise ValueError("La lista no puede estar vacía")
        return sum(numeros) / len(numeros)


# ============================================================
# Ejemplo con inyección de dependencias
# ============================================================

class ServicioUsuarios:
    """
    Capa de aplicación que depende de un repositorio abstracto.
    Gracias a la inyección de dependencias, podemos pasar un mock
    para pruebas unitarias.
    """
    def __init__(self, repo):
        self.repo = repo

    def obtener_nombres(self) -> List[str]:
        # Lógica sencilla que se puede testear sin tocar el repo real
        usuarios = self.repo.listar_todos()
        return [u.nombre for u in usuarios]


# ============================================================
# Mock simple para tests
# ============================================================

class MockUsuarioRepo:
    """Mock de repositorio para pruebas"""
    def listar_todos(self):
        from dataclasses import dataclass
        @dataclass
        class Usuario:
            id: int
            nombre: str
        return [Usuario(1, "Alice"), Usuario(2, "Bob")]


# ============================================================
# Test rápido manual
# ============================================================

if __name__ == "__main__":
    # Test CalculadoraPromedios
    calc = CalculadoraPromedios()
    print("Promedio [1,2,3]:", calc.calcular_promedio([1,2,3]))

    # Test ServicioUsuarios con mock
    servicio = ServicioUsuarios(MockUsuarioRepo())
    print("Nombres de usuarios:", servicio.obtener_nombres())
