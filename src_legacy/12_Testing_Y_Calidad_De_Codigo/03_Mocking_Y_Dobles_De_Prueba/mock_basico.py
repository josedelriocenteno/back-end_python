"""
PYTEST: MOCKING BÁSICO CON UNNTEST.MOCK
-----------------------------------------------------------------------------
Cómo usar 'MagicMock' para simular el comportamiento de objetos complejos 
sin ejecutarlos realmente.
"""

from unittest.mock import MagicMock

# 1. EL OBJETO A SIMULAR
# Imagina una clase que envía emails reales (tarda segundos y cuesta dinero).
class EmailServer:
    def send(self, to: str, body: str):
        # Lógica pesada de red...
        return True

# 2. EL TEST CON MOCK
def test_envio_notificacion_usa_el_servidor():
    """
    Queremos comprobar que nuestra lógica de negocio CORRE el método .send()
    pero sin enviar un email de verdad.
    """
    # Creamos el Mock
    mock_server = MagicMock()
    
    # Configuramos qué debe devolver cuando le llamen
    mock_server.send.return_value = True
    
    # EJECUTAMOS nuestra lógica usando el mock
    # (Imagina que enviamos el mock como dependencia)
    resultado = mock_server.send("boss@company.com", "Hola mundo")
    
    # ASSERT de Auditoría (Comprobar interacciones)
    assert resultado is True
    # ¿Se llamó a la función?
    mock_server.send.assert_called_once()
    # ¿Se llamó con los parámetros correctos?
    mock_server.send.assert_called_with("boss@company.com", "Hola mundo")

"""
¿CUÁNDO USAR MAGICMOCK?
-----------------------
- Cuando el objeto real es LENTO (Bases de datos, APIs).
- Cuando el objeto real tiene EFECTOS SECUNDARIOS (Enviar dinero, borrar S3).
- Cuando el objeto real es IMPREDECIBLE (Generadores de números aleatorios).
"""

"""
DIFERENCIA ENTRE return_value Y side_effect:
-------------------------------------------
- return_value: Devuelve siempre lo mismo (estático).
- side_effect: Puede devolver una lista de valores (uno en cada llamada) 
  o LAZAR UNA EXCEPCIÓN para probar errores.
"""
def test_simular_fallo_de_servidor():
    mock_server = MagicMock()
    # Simulamos que el servidor se cae
    mock_server.send.side_effect = ConnectionError("Servidor caído")
    
    try:
        mock_server.send("a@b.com", "msg")
    except ConnectionError:
        print("✅ Hemos testeado el manejo de errores correctamente")
