"""
EJERCICIOS PRÁCTICOS DE TESTING (CASOS DE EMPRESA)
-----------------------------------------------------------------------------
Desafíos para aplicar todo lo aprendido en una App real.
"""

import pytest

# CASO 1: EL BUG DEL REDONDEO
# Escribe un test parametrizado para una función de 'calcular_descuento' 
# que maneje correctamente flotantes usando pytest.approx.

# CASO 2: EL SERVICIO EXTERNO CRÍTICO
# Crea un test que use @patch para simular que la API de pagos (Stripe) 
# devuelve un error de 'Tarjeta Caducada'. Verifica que tu backend 
# guarda el error en la DB y envía el status code correcto.

# CASO 3: LA FIXTURE DE BASE DE DATOS
# Implementa una fixture en un archivo 'conftest.py' imaginario que use 
# 'yield' para crear un usuario administrador, lo use en los tests y lo 
# borre al terminar.

# CASO 4: TESTING ASÍNCRONO
# Tienes una función 'async def procesar_imagen()'. Escribe un test que 
# use pytest-asyncio y compruebe que la tarea termina en menos de 1 segundo.

# CASO 5: EL PROBLEMA N+1
# Describe cómo escribirías un test que detecte si un endpoint de 
# 'lista_de_pedidos' está haciendo más de una consulta SQL a la base de datos.

"""
PROYECTO FINAL DEL TEMA:
------------------------
Toma una API sencilla (CRUD de tareas) y:
1. Configura Flake8 y Mypy.
2. Crea una pipeline de GitHub Actions que pase los tests.
3. Asegura una cobertura del 85% en la carpeta de servicios.
4. Añade un pre-commit hook que pase Black.
"""
