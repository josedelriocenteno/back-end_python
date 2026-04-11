# Paralelizar Tests: La Carrera por la Velocidad

Cuando tu suite de tests crece y alcanza los 1.000 o 2.000 tests, el tiempo de ejecución puede pasar de 1 minuto a 15 minutos. Esto rompe el flujo de trabajo (Flow) del equipo. Aquí es donde entra la **Paralelización**.

## 1. Pytest-xdist
Es el plugin estándar para ejecutar tests en paralelo usando múltiples núcleos de CPU.
```bash
pip install pytest-xdist
pytest -n auto # Usa todos los núcleos disponibles
```

## 2. El reto de la Base de Datos Compartida
Si dos tests intentan usar la misma base de datos al mismo tiempo en paralelo, se borrarán los datos el uno al otro.
- **Estrategia Senior:** Crea una base de datos distinta por cada "worker" (proceso) de Pytest.
- Pytest-xdist proporciona el ID del worker. Puedes usarlo para crear nombres de DB como `test_db_worker_1`, `test_db_worker_2`, etc.

## 3. División de la Suite en Múltiples Máquinas
Si un solo servidor no es suficiente, puedes dividir tus tests en varios jobs de tu CI.
- **GitHub Actions Matrix:** Ejecuta los tests de `unit/` por un lado y los de `integration/` por otro en servidores paralelos totalmente distintos.

## 4. Tests que NO se pueden paralelizar
Hay tests que leen archivos fijos o que modifican configuraciones globales del sistema.
- Marca estos tests con `@pytest.mark.non_parallel` y configúralos para que se ejecuten secuencialmente al final de la suite.

## 5. El coste de la Paralelización
Paralelizar no es gratis.
- **Complejidad:** El código de setup (fixtures) se vuelve más difícil de escribir.
- **Consumo:** Gastas más memoria RAM y recursos en tu servidor de CI.

## Resumen: Un equipo feliz es un equipo rápido
Un desarrollador senior monitoriza el tiempo de la pipeline. Si supera los 5-10 minutos, es hora de invertir tiempo en paralelizar. Un feedback rápido permite que el equipo corrija errores al instante, manteniendo una velocidad de desarrollo alta.
