# Desnormalización: Rendimiento vs Pureza

Si la normalización es el ideal teórico de orden, la desnormalización es la respuesta pragmática a los problemas de rendimiento en aplicaciones de gran escala.

## 1. ¿Qué es la Desnormalización?

Es el proceso intencionado de introducir redundancia en la base de datos para acelerar las lecturas. No es "mal modelado" por error, es una decisión de ingeniería calculada.

## 2. ¿Cuándo desnormalizar?

Solo debes considerar desnormalizar cuando:
1.  **Rendimiento Crítico:** Una consulta con muchos JOINs es demasiado lenta y los índices no son suficientes.
2.  **Agregaciones Frecuentes:** Tu app calcula el `total_ventas` de un usuario miles de veces por segundo.
3.  **Reporting/Analítica:** Queries masivas que no necesitan consistencia al milisegundo pero sí velocidad bruta.

## 3. Técnicas Comunes de Desnormalización

### A. Columnas Calculadas (Cacheo en DB)
En lugar de sumar el precio de 100 líneas de pedido cada vez:
*   **Campo:** Añades `total_amount` a la tabla `Orders`.
*   **Riesgo:** Debes asegurar que cada vez que cambie una línea, el total se actualice (vía Triggers o lógica en Python).

### B. Atributos "Espejo"
Si en el listado de pedidos siempre muestras el `nombre_usuario`:
*   **Campo:** Copias `username` en la tabla `Orders`.
*   **Beneficio:** Ahorras un JOIN en la query más frecuente de tu app.

### C. Tablas de Resumen (Materialización)
Crear tablas que agreguen datos por hora o por día (ej: `daily_stats`). PostgreSQL permite hacer esto de forma profesional con **Vistas Materializadas** (visto en Tema 08.07).

## 4. El Coste de Desnormalizar

1.  **Mantenimiento de Datos:** Tu código Python ahora es más complejo. Debes gestionar la "verdad" en dos sitios.
    *   *Ejemplo:* Si el usuario cambia su email, ¿tienes que actualizarlo en la tabla `Users` y en las 500 facturas donde lo desnormalizaste?
2.  **Espacio en Disco:** Guardar lo mismo varias veces consume más bytes (aunque hoy en día esto suele ser secundario).
3.  **Riesgo de Inconsistencia:** Si un proceso falla a mitad de una actualización desnormalizada, tendrás datos contradictorios.

## 5. ¿Cómo manejar la desnormalización desde Python?

### Vía Aplicación (The Backend Way):
Usa transacciones para actualizar el dato original y sus copias desnormalizadas:
```python
with transaction.atomic():
    item = update_original_item()
    update_denormalized_cache_in_db(item.metadata)
```

### Vía Base de Datos (The DB Way):
Usa **Triggers** para que la base de datos se encargue automáticamente de mantener la coherencia. Es más seguro pero oculta lógica de negocio a los desarrolladores de Python.

## Resumen para el Arquitecto de Datos

*   **Normaliza primero:** Diseña tu base de datos en 3NF por defecto.
*   **Mide después:** Solo desnormaliza tras comprobar con `EXPLAIN ANALYZE` (Tema 08.06) que tienes un cuello de botella real.
*   **Documenta:** Deja claro qué columnas son redundantes para que otros desarrolladores no intenten borrarlas pensando que es un error.
*   **Consistencia Eventual:** Acepta que en sistemas grandes, el dato desnormalizado puede tardar unos segundos en ser idéntico al original.
