# Logging por Entornos: Dev vs. Prod

En una aplicación profesional, no queremos la misma cantidad de logs en nuestro ordenador que en el servidor de producción. Aquí te explico cómo gestionarlo.

## 1. Nivel de Log Dinámico
Ajusta el nivel de log mediante variables de entorno.
*   **Desarrollo (DEV):** `DEBUG`. Queremos ver cada detalle para entender qué hace el código.
*   **Producción (PROD):** `INFO` o `WARNING`. Solo queremos ver los eventos importantes y errores para no saturar los discos y ahorrar costes de almacenamiento.

```python
import os
import logging

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)
```

## 2. Destinos Diferentes (Handlers)
*   **Local:** Los logs van a la terminal (`StreamHandler`) para verlos mientras programamos.
*   **Producción:** Los logs suelen enviarse a un servicio centralizado (Cloud Logging, ELK Stack, Datadog) o a archivos rotativos para que no llenen el disco del servidor.

## 3. Formato de los Mensajes
*   **Local:** Formato amigable para humanos, con colores y timestamps sencillos.
*   **Producción:** **Logs Estructurados (JSON)**. Las máquinas no leen frases, leen campos. Un log en JSON permite hacer búsquedas potentes por ID de usuario, tipo de error o nombre del servidor.

## 4. Gestión de Secretos en Logs
**REGLA DE ORO:** Nunca imprimas en el log:
*   Contraseñas.
*   Tokens de API.
*   Datos personales (PII) como DNI o tarjeta de crédito.
Implementa "filtros" en tu logger para censurar estas palabras si aparecen accidentalmente.

## 5. El "Error silencioso" de los Logs
Cuidado con hacer logs pesados dentro de bucles de millones de filas. Hacer un print por cada fila en un proceso de Big Data puede ralentizar tu pipeline un 500% y generar gigabytes de basura innecesaria.

## Resumen: Adaptabilidad
El logging profesional es aquel que se adapta al lugar donde corre. Aprende a usar variables de entorno para decidir qué contar y a quién, manteniendo siempre el equilibrio entre visibilidad y rendimiento.
