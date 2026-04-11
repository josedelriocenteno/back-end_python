# Streaming BigQuery: Ingesta en Tiempo Real

A veces, esperar a que un archivo se cargue cada hora no es suficiente. Necesitas ver los datos en el dashboard segundos después de que ocurra la acción. Para eso usamos la **Streaming API** de BigQuery.

## 1. ¿Cómo funciona?
En lugar de subir un archivo, envías filas individuales directamente a BigQuery mediante una petición HTTP (normalmente a través de la SDK de Python).
- El dato está disponible para ser consultado en unos segundos.

## 2. La API de Escritura de Almacenamiento (Storage Write API)
Es la forma moderna y recomendada por Google para hacer streaming.
- **Ventaja:** Más barata y con mayor rendimiento que la API de streaming clásica.
- **Tipos de entrega:** `At-least-once` (Al menos una vez) o `Exactly-once` (Exactamente una vez, para evitar duplicados).

## 3. Casos de Uso
- **Monitorización de Fraude:** Detectar un robo de tarjeta en el momento.
- **Logística:** Seguimiento de repartidores en un mapa en vivo.
- **E-commerce:** Ver las tendencias de búsqueda de los usuarios en el mismo instante en que ocurren.

## 4. El coste del Streaming
A diferencia de la carga por lotes (Batch), el streaming **no es gratis**.
- Pagas por la cantidad de MB insertados. 
- **Tip Senior:** No uses streaming para todo. Si un reporte solo lo mira el jefe una vez al día, usa Batch y ahorra dinero a la empresa.

## 5. Buffer de Calidad
Como el dato entra en tiempo real, es difícil validarlo antes de que llegue a la tabla.
- **Estrategia:** Inserta en una tabla `raw` mediante streaming y ten un proceso ligero que mueva esos datos a la tabla final cada pocos minutos, realizando las validaciones de calidad necesarias.

## Resumen: Agilidad Extrema
El streaming convierte a BigQuery en un sistema vivo. Permite que el negocio reaccione al mundo real con una latencia mínima, abriendo la puerta a casos de uso analíticos que antes eran imposibles con modelos de carga tradicionales.
