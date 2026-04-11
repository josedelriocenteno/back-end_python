# Errores Comunes en ETL: Cómo evitar el desastre

Incluso el mejor pipeline fallará tarde o temprano. Saber qué suele romperse te permitirá construir sistemas más resilientes.

## 1. El cambio de esquema (Schema Drift)
La base de datos origen añade una columna nueva o, peor aún, cambia un tipo de dato (de Int a String).
- **Efecto:** El pipeline se detiene con un error de tipo.
- **Prevención:** Usa validaciones de esquema o "Data Contracts".

## 2. Datos Duplicados
Un pipeline falla a la mitad, se reintenta y vuelve a insertar los datos que ya estaban.
- **Efecto:** Tu reporte de ventas dice que has vendido el doble de lo real.
- **Prevención:** Usa **Idempotencia** (ver sección 03) y cargas basadas en un ID único.

## 3. Problemas de Red y Timeout
Intentar bajar 1GB de una API que se corta a los 30 segundos.
- **Prevención:** Paginación (bajar datos en trozos pequeños de 100 en 100) y lógica de reintentos con espera exponencial (Exponential Backoff).

## 4. El "Silent Failure" (Fallo Silencioso)
El pipeline termina con "Éxito", pero la fuente de datos ha devuelto 0 registros porque la API estaba vacía.
- **Efecto:** Tus dashboards están vacíos pero no hay alertas.
- **Prevención:** Crea alertas basadas en métricas de volumen: "Alerta si un pipeline carga 80% menos datos de lo habitual".

## 5. Hardcoding de rutas y secretos
Escribir `/home/usuario/datos.csv` o la API KEY en el medio del código Python.
- **Prevención:** Usa variables de entorno y parámetros configurables.

## Resumen: Diseña para el Fallo
Un Junior asume que el pipeline siempre funcionará. Un Senior asume que el pipeline va a fallar hoy mismo y escribe código que detecta el error, avisa por Slack y permite re-ejecutarlo sin corromper los datos.
