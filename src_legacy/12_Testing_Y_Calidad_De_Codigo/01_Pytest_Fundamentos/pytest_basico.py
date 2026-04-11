"""
PYTEST: ESTRUCTURA PROFESIONAL DE UN TEST
-----------------------------------------------------------------------------
Cómo escribir tests que sean fáciles de leer, ejecutar y mantener.
"""

# No necesitamos importar nada complejo, pytest detecta funciones con 'test_'
import pytest

# 1. EL CÓDIGO A TESTEAR (Imagina que esto está en src/utils.py)
def calcular_impuesto(monto: float, porcentaje: float) -> float:
    if monto < 0:
        raise ValueError("El monto no puede ser negativo")
    return round(monto * (porcentaje / 100), 2)

# 2. EL TEST (Sigue el patrón AAA: Arrange, Act, Assert)
def test_calcular_impuesto_basico():
    """
    Caso estándar: Calcula el 21% de 100.
    """
    # ARRANGE (Preparar: datos de entrada)
    monto = 100.0
    iva = 21.0
    esperado = 21.0
    
    # ACT (Actuar: ejecutar la función)
    resultado = calcular_impuesto(monto, iva)
    
    # ASSERT (Afirmar: comprobar el resultado)
    assert resultado == esperado
    assert isinstance(resultado, float)

# 3. TEST DE EXCEPCIONES
def test_calcular_impuesto_monto_negativo():
    """
    Comprobar que la función lanza el error correcto ante datos inválidos.
    """
    with pytest.raises(ValueError) as excinfo:
        calcular_impuesto(-50, 10)
    
    assert "monto no puede ser negativo" in str(excinfo.value)

# 4. TEST DE LÍMITES (Edge Cases)
def test_calcular_impuesto_cero():
    assert calcular_impuesto(0, 21) == 0.0

"""
CÓMO EJECUTAR LOS TESTS:
-----------------------------------------------------------------------------
1. Instala: pip install pytest
2. Ejecuta todo: pytest
3. Ver detalles: pytest -v
4. Parar al primer fallo: pytest -x

CONSEJO SENIOR:
---------------
Usa nombres descriptivos. 'test_calculo' es malo. 
'test_calcular_impuesto_redondea_a_dos_decimales' es excelente porque si 
falla, el log te dice exactamente qué comportamiento se ha roto.
"""
