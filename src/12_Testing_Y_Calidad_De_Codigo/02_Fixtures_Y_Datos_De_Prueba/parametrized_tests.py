"""
PYTEST: TESTS PARAMETRIZADOS (DRY - Don't Repeat Yourself)
-----------------------------------------------------------------------------
Cómo probar múltiples casos de entrada/salida sin escribir 20 funciones 
casi idénticas.
"""

import pytest

def es_password_segura(password: str) -> bool:
    """Función simple que queremos testear a fondo."""
    return len(password) >= 8 and any(char.isdigit() for char in password)

# 1. PARAMETRIZACIÓN BÁSICA
@pytest.mark.parametrize(
    "password, resultado_esperado",
    [
        ("12345678", True),      # Válida (Larga + número)
        ("abc12345", True),      # Válida
        ("1234567", False),      # Inválida (Corta)
        ("abcdefghi", False),    # Inválida (Sin números)
        ("", False),             # Inválida (Vacía)
        ("A-b-c-1-2-3", True),   # Válida (Con símbolos)
    ]
)
def test_validar_password(password, resultado_esperado):
    assert es_password_segura(password) == resultado_esperado

# 2. PARAMETRIZACIÓN DE FIXTURES (Avanzado)
@pytest.fixture(params=["mysql", "postgresql", "sqlite"])
def db_engine(request):
    """Este test se ejecutará 3 veces, una con cada motor."""
    return f"Motor: {request.param}"

def test_db_connection(db_engine):
    print(f"Probando conexión con {db_engine}")
    assert "Motor:" in db_engine

"""
VENTAJAS:
---------
1. COBERTURA: Es tan fácil añadir un caso nuevo como añadir una fila a la lista.
2. INDEPENDENCIA: Si el caso 3 falla, Pytest te mostrará que ha fallado ese 
   exacto, pero los demás (1, 2, 4, 5, 6) seguirán pasando.
3. LIMPIEZA: Reduce drásticamente el 'Boilerplate' (código repetitivo) de 
   tus carpetas de test.
"""
