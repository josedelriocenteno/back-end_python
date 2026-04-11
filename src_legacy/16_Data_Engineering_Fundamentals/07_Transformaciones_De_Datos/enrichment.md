# Enrichment: Añadiendo valor a los datos

El enriquecimiento (Data Enrichment) consiste en mejorar los datos crudos añadiendo información externa o calculando nuevos campos.

## 1. Unión con Tablas Maestras (Lookups)
Es el enriquecimiento más común.
- **Ejemplo:** Tienes un ID de tienda en el pedido. Cruzas esa tabla con la de "Tiendas" para añadir el nombre de la ciudad y el encargado.

## 2. Enriquecimiento Geográfico (Geo-Enrichment)
A partir de una IP o una coordenada:
- Obtener el País, Ciudad y Código Postal (usando bases de datos como MaxMind).
- Esto permite al negocio ver mapas de calor de ventas.

## 3. Enriquecimiento Temporal
A partir de una fecha simple (`2024-03-15`):
- Añadir si era fin de semana (`is_weekend`).
- Añadir si era día festivo (`is_holiday`).
- Calcular el trimestre (`Q1`).

## 4. Clasificación y Scoring
- **Sentiment Analysis:** Pasar el texto de un comentario por una IA para añadir una columna con `Positivo`, `Neutro` o `Negativo`.
- **Lead Scoring:** Basado en la actividad decidiéndo si el usuario es un `Hot Lead` o `Cold Lead`.

## 5. El reto: La disponibilidad de la fuente externa
Si tu enriquecimiento depende de una API externa:
- ¿Qué pasa si la API está caída?
- ¿El pipeline debe fallar o puede seguir con el dato sin enriquecer?
- **Caché:** Guarda los resultados de la API externa para no consultarla un millón de veces para el mismo ID.

## Resumen: De Dato a Información
El enriquecimiento es el paso donde el dato deja de ser algo técnico y se convierte en algo rico en contexto para el negocio. Un buen enriquecimiento hace que un dashboard sea infinitamente más útil.
