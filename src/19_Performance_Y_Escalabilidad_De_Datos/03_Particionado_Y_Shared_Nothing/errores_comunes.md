# Errores Comunes al Particionar

El particionado no es una bala de plata. Si se aplica mal, puede complicar el desarrollo y empeorar el rendimiento. Estos son los errores que debes evitar.

## 1. Over-partitioning (Demasiadas particiones)
*   **El error:** Crear una partición por cada día para una tabla que solo recibe 1.000 filas al día. En un año tendrás 365 tablas.
*   **El impacto:** El motor de la base de datos se vuelve lento gestionando miles de archivos de metadatos. Se consume mucha memoria solo para abrir la tabla.
*   **Solución:** Agrupa. Si tienes pocos datos, particiona por **Mes** o por **Año**.

## 2. No filtrar por la Clave de Partición
*   **El error:** Particionas por `fecha` pero tus queries filtran por `customer_id`.
*   **El impacto:** El motor tiene que hacer un escaneo en TODAS las particiones para encontrar al cliente. El rendimiento es igual o peor que no tener particiones.
*   **Solución:** Asegúrate de que las consultas más frecuentes incluyan la clave de partición.

## 3. Olvidar la Retención de Datos
*   **El error:** Crear particiones dinámicamente pero nunca borrarlas.
*   **El impacto:** Te quedas sin espacio en disco o alcanzas el límite de archivos abiertos del sistema operativo.
*   **Solución:** Automatiza un script de limpieza que haga `DROP TABLE` de las particiones más viejas de X meses.

## 4. Updates en la Clave de Partición
*   **El error:** Cambiar el valor de la columna que define la partición (ej: cambiar la fecha de una factura de 2023 a 2024).
*   **El impacto:** La base de datos tiene que "mover" físicamente la fila de una tabla a otra. Es una operación costosa y lenta que puede fallar si no está bien configurada (en Postgres requiere habilitar `ENABLE ROW MOVEMENT`).
*   **Solución:** Elige una clave de partición que sea lo más **inmutable** posible.

## 5. Índices Globales Inexistentes
En la mayoría de los sistemas particionados, los índices son locales a cada partición.
*   **El impacto:** Si buscas por un ID único en todo el sistema sin decir la partición, el motor debe consultar todos los índices locales uno por uno.
*   **Solución:** Acepta este compromiso o incluye la clave de partición en tus filtros de búsqueda siempre que sea posible.

## Resumen: Menos es Más
El particionado es para domar la complejidad física de los datos, no para aumentarla. Úsalo con moderación, elige claves que no cambien y que uses en tus queries, y mantén el número de particiones bajo control para obtener todos los beneficios sin los dolores de cabeza.
