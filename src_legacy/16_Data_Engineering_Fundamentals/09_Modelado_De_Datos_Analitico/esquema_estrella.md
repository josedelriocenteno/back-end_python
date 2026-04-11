# Esquema Estrella (Star Schema): El estándar de oro

El esquema estrella es la implementación más simple y efectiva del modelado dimensional. Se llama así porque visualmente parece una estrella con una tabla de hechos en el centro.

## 1. La Estructura
- **Centro:** Una única tabla de Hechos (`fact_sales`). Contiene las métricas y las claves foráneas a las dimensiones.
- **Puntas:** Varias tablas de Dimensiones (`dim_products`, `dim_customers`) conectadas directamente al centro.
- **Regla:** Las dimensiones NO se conectan entre sí. Solo se conectan a la tabla de hechos.

## 2. Ventajas del Esquema Estrella
- **Sencillez:** Las consultas SQL solo requieren de un `JOIN` entre la tabla de hechos y la dimensión que necesites.
- **Rendimiento:** Al haber pocos `JOINs`, los motores de base de datos pueden optimizar la query de forma agresiva.
- **Fácil de entender:** Es el modelo que mejor entienden las herramientas de BI como Tableau o PowerBI.

## 3. Desnormalización (Denormalization)
En el esquema estrella, las dimensiones están **desnormalizadas**. Esto significa que aceptamos tener datos repetidos (ej: El nombre de la categoría del producto se repite en cada fila de la dimensión productos) para evitar tener otra tabla de categorías.

## 4. Por qué es mejor para Big Data
Como el almacenamiento (disco) es barato y el procesamiento (CPU/Memoria) es caro, preferimos tener tablas más anchas (repetidas) si eso nos ahorra hacer `JOINs` complejos en tiempo de ejecución.

## 5. Cuándo usarlo
Es la recomendación por defecto para cualquier Data Warehouse. Solo deberías considerar otras opciones si tienes dimensiones extremadamente grandes o jerarquías muy complejas.

## Resumen: Simplicidad es Velocidad
El esquema estrella es la arquitectura que permite que una empresa pase de "tener datos" a "usar datos". Reduce la fricción técnica y maximiza la velocidad de respuesta del sistema analítico.
