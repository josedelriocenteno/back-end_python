# Ejemplos Reales: El Modelo que Escala

Vamos a ver cómo se transforma un modelo real de una App a un Data Warehouse para ganar rendimiento.

## Caso: Plataforma de E-commerce

### 1. El Origen (OLTP - PostgreSQL) - Normalizado
Tenemos 10 tablas: `usuarios`, `pedidos`, `lineas_pedido`, `productos`, `categorias`, `marcas`, `tiendas`, `paises`, `metodos_pago`, `envios`.
*   **Escenario:** El usuario pulsa "Comprar" y el backend inserta 1 fila en `pedidos` y 3 en `lineas_pedido`. Es rápido y seguro.
*   **Problema:** El analista de marketing quiere saber: "Ventas por categoría de este mes en España". La query tiene 7 JOINS. Tarda 15 segundos. Si marketing lanza 100 queries, la web empieza a ir lenta.

### 2. El Destino (OLAP - BigQuery) - Esquema Estrella
Creamos un modelo de 1 Tabla de Hechos y 4 Dimensiones:
*   **Hechos:** `fact_ventas_linea` (id_producto, id_tiempo, id_cliente, id_tienda, cantidad, total_linea).
*   **Dimensiones:** `dim_producto` (incluye marca y categoría), `dim_cliente` (incluye país), `dim_tienda`, `dim_tiempo` (fechas ya calculadas).
*   **Resultado:** La misma query de marketing ahora tiene 2 JOINS. Tarda 1.5 segundos. No afecta a la web de producción.

### 3. Optimizando un Cuello de Botella real
**Problema:** La columna `nombre_producto` es la más consultada.
*   **Mejora:** Aunque estemos en estrella, desnormalizamos un paso más y ponemos `nombre_producto` también en la tabla de **Hechos**.
*   **Resultado:** Muchas queries ya no necesitan ningún `JOIN` para sacar informes básicos. El rendimiento sube otro 30%.

### 4. Manejando el Histórico (SCD Tipo 2)
Un producto cambia de precio un lunes.
*   Si solo tenemos el precio actual, el informe de ventas del domingo saldrá mal (calculado con el precio de hoy).
*   En el modelo escalable, guardamos `precio_historico` en la línea del pedido en el momento de la compra. **Inmutabilidad = Precisión**.

## Resumen: De la Transacción a la Respuesta
El modelado para escala consiste en anticipar cómo se van a leer los datos. Mientras que la App necesita seguridad y detalle, el análisis necesita velocidad y pre-procesamiento. Entender este camino es el núcleo del trabajo de un Data Engineer.
