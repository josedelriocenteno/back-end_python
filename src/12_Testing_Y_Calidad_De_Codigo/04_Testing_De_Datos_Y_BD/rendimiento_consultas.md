# Rendimiento de Consultas en Tests: Detectando el N+1

Los tests no solo sirven para ver si el dato es correcto, también pueden servir para detectar problemas de rendimiento antes de que lleguen a producción, como el temido **Problema N+1**.

## 1. ¿Qué es el Problema N+1?
Ocurre cuando haces una consulta para obtener 100 usuarios, y luego, dentro de un bucle, haces 100 consultas más para obtener el perfil de cada uno.
- Resultado: 101 consultas a la DB en lugar de una sola con un `JOIN`.

## 2. Cómo detectarlo con Tests
Existen plugins para Pytest (como `pytest-sqlalchemy-mock` o simplemente custom helpers) que permiten contar cuántas queries se han disparado durante un test.
```python
def test_obtener_lista_usuarios_no_hace_queries_extra(db_session, count_queries):
    # ARRANGE
    poblar_db(db_session, 100) # Creamos 100 usuarios
    
    # ACT
    with count_queries() as queries:
        obtener_todos_los_usuarios(db_session)
    
    # ASSERT: Solo debería haber hecho UNA query
    assert len(queries) == 1
```

## 3. Test de "Límites de Carga" (Basic Load Test)
Si una query tarda 10ms con 5 filas, pero tarda 2 segundos con 1.000 filas, probablemente te falte un **Índice**.
- Puedes crear un test que use Faker para meter un volumen realista de datos (ej: 5.000 registros) y poner un assertion sobre el tiempo máximo de ejecución:
```python
import time

def test_rendimiento_busqueda_productos(db_session):
    # Generar carga masiva
    ...
    start = time.time()
    buscar_productos("laptop")
    end = time.time()
    
    assert (end - start) < 0.1 # Debe tardar menos de 100ms
```

## 4. SQL Explain en los Tests
Para queries críticas, tu test puede ejecutar un `EXPLAIN ANALYZE` y verificar que la base de datos está usando un **Index Scan** en lugar de un **Seq Scan** (escaneo secuencial lento).

## Resumen: Seniority en Performance
Un desarrollador senior no espera a que el servidor de producción vaya lento para optimizar. Usa la suite de tests para "blindar" el rendimiento, asegurando que cualquier cambio de código que introduzca una ineficiencia sea detectado en la pipeline de integración.
