# Deduplicación: El enemigo de los números reales

Los duplicados son la pesadilla de cualquier analista. Hacen que las métricas de crecimiento y dinero parezcan mejores de lo que son.

## 1. Por qué ocurren duplicados
- **Reintentos de Ingesta:** El pipeline falla tras insertar pero antes de marcar como "Terminado". Al reintentar, inserta de nuevo.
- **Fuentes Duplicadas:** Dos sistemas envían el mismo evento de usuario.
- **Errores de Join:** Hacer un cruce de tablas incorrecto que multiplica las filas.

## 2. Tipos de Duplicados
- **Exactos:** Todas las columnas son idénticas. Fáciles de limpiar (`DISTINCT`).
- **Lógicos:** El ID del usuario es el mismo, pero cambian otros campos (ej: timestamp de conexión). Requiere decidir con cuál quedarse.

## 3. Estrategias de Deduplicación
- **First Seen:** Quedarse con la primera vez que vimos el dato.
- **Last Seen:** Quedarse con la versión más reciente (ej: actualización de perfil).
- **Primary Key Enforcement:** Confiar en que la base de datos de destino no nos deje insertar un ID repetido.

## 4. Implementación en SQL (Window Functions)
El método profesional usando `ROW_NUMBER()`:
```sql
WITH deduplicated AS (
  SELECT *,
    ROW_NUMBER() OVER(PARTITION BY order_id ORDER BY updated_at DESC) as row_num
  FROM raw_orders
)
SELECT * FROM deduplicated WHERE row_num = 1
```

## 5. Deduplicación en Streaming
Mucho más complejo. Requiere una "ventana de tiempo". No puedes comparar un evento de hoy con uno de hace 3 años en tiempo real. Usamos un Buffer (ej: Redis) de los últimos N minutos para descartar repetidos inmediatos.

## Resumen: Una Verdad Única
Los duplicados destruyen la credibilidad del dato. Tu éxito como ingeniero de datos depende de tu capacidad para asegurar que cada acción del mundo real se represente exactamente una vez en tus tablas finales.
