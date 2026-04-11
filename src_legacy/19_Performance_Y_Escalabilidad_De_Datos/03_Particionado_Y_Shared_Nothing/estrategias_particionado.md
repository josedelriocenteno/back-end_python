# Estrategias de Particionado: ¿Cómo elegir?

No existen reglas fijas, pero sí estrategias probadas según el caso de uso. Elegir mal la clave de partición puede ser peor que no particionar nada.

## 1. La Estrategia Temporal (Time-based)
Es la más usada en Data Engineering (90% de los casos).
*   **Cuándo:** Para logs, eventos, ventas, telemetría.
*   **Por qué:** 
    1. Solemos consultar datos recientes (los últimos 30 días).
    2. Facilita las políticas de retención (borrar datos viejos).
    3. Los datos históricos casi nunca cambian.

## 2. La Estrategia Geográfica (Tenant-based)
*   **Cuándo:** Aplicaciones SaaS donde cada cliente es independiente.
*   **Por qué:** Permite que los datos de "Amazon" no se mezclen físicamente con los de "eBay". Mejora la seguridad y permite mover un cliente grande a su propio servidor de forma sencilla.

## 3. La Estrategia por Carga (Balanced Hash)
*   **Cuándo:** Tienes una tabla gigante de "Usuarios" que se consulta por ID desde mil sitios a la vez.
*   **Por qué:** Evitas los "Hotspots" (puntos calientes). Repartes la carga de lectura/escritura equitativamente entre todos los discos o nodos.

## 4. Factores a tener en cuenta

### A. Cardinalidad
*   No particiones por una columna con pocos valores (ej: `sexo`). Solo tendrías 2 particiones gigantes. No sirve de nada.
*   No particiones por una columna con demasiados valores únicos (ej: `email`). Tendrías millones de particiones minúsculas, lo cual colapsa el sistema de archivos de la base de datos.
*   **El punto "G":** Busca entre 10 y 1.000 particiones por tabla.

### B. Patrones de Acceso
*   Mira tus queries habituales. Si el 99% de tus queries tienen `WHERE id_empresa = X`, particiona por `id_empresa`. Si particionas por `fecha`, el motor tendrá que mirar TODAS las particiones de fecha para encontrar a esa empresa, arruinando el rendimiento.

## 5. Particionado Multinivel
Puedes combinar estrategias.
*   **Nivel 1:** Particionado por `Año` (Rango).
*   **Nivel 2:** Dentro de cada año, particionado por `Región` (Lista).
Solo recomendado para volúmenes de datos verdaderamente masivos.

## Resumen: Diseña para la Query
La mejor estrategia de particionado es la que se alinea con cómo vas a preguntar por los datos. Un sistema bien particionado minimiza el trabajo de la base de datos, permitiéndole ir directamente al grano e ignorar el 99% de los datos irrelevantes.
