# mocks_y_stubs.py

"""
MÓCKS Y STUBS EN PYTHON
========================

Objetivo:
---------
Aislar componentes en pruebas unitarias, evitando efectos colaterales y
dependencias externas como bases de datos, APIs o servicios de terceros.

Conceptos clave:
----------------
1. Stub: versión simplificada de un componente que devuelve datos fijos.
2. Mock: objeto que registra interacciones y permite verificar llamadas.
3. Test aislado: probar una unidad de código sin depender de otros componentes.

Ejemplo orientado a tu caso:
----------------------------
Imagina que estás desarrollando un servicio de usuarios que obtiene información
desde un repositorio, pero quieres testear la lógica sin tocar la DB real.
"""

from typing import List

# ============================================================
# Clases del sistema real
# ============================================================

class RepositorioUsuarios:
    def listar_todos(self) -> List[str]:
        # Simula acceso a base de datos real
        raise NotImplementedError("Conexión a base de datos no implementada")

class ServicioUsuarios:
    def __init__(self, repo: RepositorioUsuarios):
        self.repo = repo

    def nombres_en_mayusculas(self) -> List[str]:
        return [nombre.upper() for nombre in self.repo.listar_todos()]

# ============================================================
# STUB: datos predecibles para pruebas
# ============================================================

class RepositorioUsuariosStub:
    def listar_todos(self) -> List[str]:
        # Datos fijos para pruebas
        return ["Alice", "Bob", "Charlie"]

# ============================================================
# MOCK: registra llamadas para verificación
# ============================================================

class RepositorioUsuariosMock:
    def __init__(self):
        self.llamadas = 0

    def listar_todos(self) -> List[str]:
        self.llamadas += 1
        return ["TestUser1", "TestUser2"]

# ============================================================
# Uso práctico
# ============================================================

if __name__ == "__main__":
    # Usando stub para pruebas rápidas
    servicio_stub = ServicioUsuarios(RepositorioUsuariosStub())
    print("Con stub:", servicio_stub.nombres_en_mayusculas())
    # -> ['ALICE', 'BOB', 'CHARLIE']

    # Usando mock para verificar interacciones
    mock_repo = RepositorioUsuariosMock()
    servicio_mock = ServicioUsuarios(mock_repo)
    print("Con mock:", servicio_mock.nombres_en_mayusculas())
    print("Cantidad de llamadas al mock:", mock_repo.llamadas)
    # -> 1

"""
Explicación orientada a tu caso:
--------------------------------
Cuando desarrolles sistemas backend o pipelines de datos:

- Los stubs te permiten probar lógica de negocio sin depender de bases de datos reales.
- Los mocks permiten comprobar que tus clases interactúan correctamente con sus dependencias.
- Esto te prepara para escribir código testable y profesional, algo fundamental para mantener calidad en proyectos grandes.
"""
