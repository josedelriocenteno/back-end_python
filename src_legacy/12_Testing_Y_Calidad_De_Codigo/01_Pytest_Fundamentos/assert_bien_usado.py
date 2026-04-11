"""
PYTEST: ASSERT BIEN USADO
-----------------------------------------------------------------------------
El 'assert' es el corazón del test. No te limites a comprobar igualdad.
"""

import pytest

def test_comparaciones_complejas():
    # Listas
    lista_original = [1, 2, 3]
    assert 2 in lista_original
    assert len(lista_original) == 3
    
    # Diccionarios (muy común en APIs)
    config = {"env": "prod", "debug": False, "version": 1.5}
    assert "env" in config
    assert config["debug"] is False
    
    # Comprobar tipos
    assert isinstance(config["version"], float)

def test_comparacion_flotantes():
    """
    ¡CUIDADO! Nunca compares flotantes con '==' directo debido a la 
    precisión binaria (0.1 + 0.2 != 0.3 en Python).
    """
    monto = 0.1 + 0.2
    # assert monto == 0.3  # <-- Esto fallaría injustamente
    
    # FORMA CORRECTA: Usa pytest.approx
    assert monto == pytest.approx(0.3)

def test_verificar_multiples_condiciones():
    username = "admin_super"
    
    # Puedes encadenar asserts o usar lógica booleana
    assert username.startswith("admin") and len(username) > 5

"""
RECOMENDACIÓN SENIOR:
---------------------
No pongas 50 asserts en un solo test si prueban cosas distintas. Si el 
primer assert falla, los otros 49 no se ejecutan y pierdes información.
Intenta que cada test tenga una 'razón única' para fallar.
"""
