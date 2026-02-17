# Organización de Tests en Proyectos Grandes

A medida que tu App crece, no puedes tener todos los tests en un solo archivo. Necesitas una estructura que Pytest entienda y que sea fácil de navegar para el equipo.

## 1. La Carpeta `tests/`
La convención estándar es tener una carpeta dedicada llamada `tests/` en la raíz del proyecto.
```text
proyecto/
├── src/
│   ├── auth.py
│   └── orders.py
└── tests/
    ├── conftest.py          # Fixtures globales
    ├── unit/
    │   ├── test_auth.py
    │   └── test_orders.py
    └── integration/
        └── test_db_orders.py
```

## 2. Nomenclatura Obligatoria (Discovery)
Pytest busca por defecto:
- Archivos que empiecen por `test_*.py` o terminen en `*_test.py`.
- Funciones que empiecen por `test_`.
- Clases que empiecen por `Test`.

## 3. El archivo `conftest.py`
Es un archivo especial de Pytest. Las fixtures definidas aquí están disponibles para TODOS los archivos de test de esa carpeta y subcarpetas **sin necesidad de importarlas**.
- Úsalo para configurar la base de datos de test, clientes de API o mocks compartidos.

## 4. Clasificación por Marcadores (Marks)
Puedes etiquetar tests para ejecutarlos por separado.
```python
import pytest

@pytest.mark.slow
def test_pago_real_con_stripe():
    ...
```
Luego puedes ejecutar solo los rápidos: `pytest -m "not slow"`.

## 5. Tests dentro del código (No Recomendado)
Aunque Python permite poner tests dentro del mismo archivo `.py` de la lógica, en backend profesional se considera una mala práctica:
- Ensucia el código de producción.
- Aumenta el tamaño del paquete desplegado.
- Dificulta la separación de dependencias de test y de prod.

## Resumen: Estructura Espejo
Un buen consejo es que la estructura de `tests/unit/` sea un "espejo" de tu carpeta `src/`. Si tienes un archivo `src/services/email.py`, deberías tener un `tests/unit/services/test_email.py`. Esto hace que encontrar un test sea instantáneo.
