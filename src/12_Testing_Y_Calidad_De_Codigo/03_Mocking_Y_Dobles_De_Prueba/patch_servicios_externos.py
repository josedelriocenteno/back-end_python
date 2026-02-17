"""
PYTEST: PATCHING (INTERCEPTAR CÓDIGO EXTERNO)
-----------------------------------------------------------------------------
A veces no podemos pasar el Mock como argumento (Inyección). En esos 
casos usamos 'patch' para interceptar una función en todo el sistema.
"""

from unittest.mock import patch
import requests # Imagina que nuestra App usa requests

# 1. LA FUNCIÓN QUE QUEREMOS TESTEAR
def obtener_clima(ciudad: str):
    # Llama a una API externa real
    response = requests.get(f"https://api.weather.com/{ciudad}")
    return response.json()

# 2. EL TEST CON PATCH
# El string debe ser el camino completo hacia donde se USA el objeto.
@patch("requests.get")
def test_obtener_clima_sin_internet(mock_get):
    """
    'mock_get' es inyectado automáticamente por el decorador @patch.
    """
    # Configuramos el mock para que devuelva un objeto con .json()
    mock_response = MagicMock()
    mock_response.json.return_value = {"temp": 25, "cielo": "despejado"}
    mock_get.return_value = mock_response
    
    # Ejecutamos
    clima = obtener_clima("Madrid")
    
    # Verificamos
    assert clima["temp"] == 25
    mock_get.assert_called_once_with("https://api.weather.com/Madrid")

"""
EL PELIGRO DEL PATCH:
--------------------
El principal error es parchear el sitio donde se DEFINE la función en lugar 
de donde se USA. 
- Mal: @patch("requests.get") si 'requests' se importó como 'from requests import get'.
- Bien: @patch("tu_proyecto.servicios.requests.get").
"""

"""
PATCH COMO CONTEXT MANAGER:
---------------------------
Si solo quieres el mock durante 3 líneas de código:
"""
def test_patch_temporal():
    with patch("os.remove") as mock_remove:
        # Aquí os.remove es de mentira
        pass
    # Aquí os.remove vuelve a ser la real
