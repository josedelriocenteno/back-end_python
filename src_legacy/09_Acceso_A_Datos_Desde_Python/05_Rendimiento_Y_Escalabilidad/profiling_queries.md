# Profiling: Midiendo el rendimiento del Acceso a Datos

"Lo que no se mide, no se puede optimizar". Antes de añadir índices o cambiar el ORM por SQL puro, debemos saber dónde se pierde el tiempo.

## 1. Logs de SQL (El primer nivel)
Activa el logueo de todas las consultas generadas por SQLAlchemy.
```python
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

## 2. Herramientas de Inspección (DevTools)

### SQLAlchemy-Utils / Query Counter
Existen pequeñas utilidades para contar cuántas queries se lanzan en un bloque de código.
```python
with count_queries() as counter:
    do_something()
print(f"Queries ejecutadas: {counter.count}") # ¡Si ves 100, tienes un N+1!
```

### Flask-DebugToolbar / Django Debug Toolbar
Si usas Web Frameworks pesados, estas barras te muestran en tiempo real cada query, su tiempo y si hay duplicados.

## 3. Profiling de Aplicación (Yappi / cProfile)
Si sospechas que el problema no es el SQL, sino que Python tarda mucho filtrando los resultados:
*   Usa **Yappi** (Yet Another Python Profiler) para ver cuánto tiempo gasta cada función.

## 4. Análisis de la Base de Datos (Slow Query Logs)
PostgreSQL puede registrar las queries que tardan más de X milisegundos.
*   Pide a tu DBA activar `log_min_duration_statement = 500ms`.
*   Usa `pg_stat_statements` para ver el acumulado de consumo de recursos.

## 5. El impacto de la Serialización
A veces, el 50% del tiempo de una API no es SQL, sino **Pydantic** convirtiendo objetos ORM complejos a JSON.
*   **Optimización:** Devuelve solo los campos necesarios (Proyecciones).

## 6. Checklist de Diagnóstico

1.  [ ] ¿He activado los logs de SQL para ver qué está pasando realmente?
2.  [ ] ¿Cuántas queries se lanzan por cada petición HTTP? (Ideal: < 5).
3.  [ ] ¿Cuál es el tiempo de ejecución en la DB vs el tiempo de respuesta total?
4.  [ ] ¿He usado `EXPLAIN ANALYZE` en las queries que aparecen como lentas?

## Resumen: Optimiza con Datos, no con Intuición

Muchos desarrolladores "optimizan" añadiendo índices al azar. Un arquitecto senior hace profiling, identifica el cuello de botella (probablemente un N+1 o falta de pooling) y aplica la solución quirúrgica necesaria.
