# Errores Comunes en Logging

Incluso usando librerías profesionales, es fácil caer en trampas que hacen que tus logs sean inútiles o, peor aún, peligrosos.

## 1. Logging de baja calidad ("I was here")
*   **Error:** `logger.info("Empieza el proceso")`, `logger.info("Sigue el proceso")`, `logger.info("Fin")`.
*   **Solución:** Los logs deben aportar valor. ¿Qué proceso? ¿Con qué parámetros? ¿Cuántas filas se esperan procesar?

## 2. No usar `exc_info` en los errores
*   **Error:** `except Exception as e: logger.error(f"Error: {e}")`.
*   **Consecuencia:** Solo verás el nombre del error (ej: `KeyError: 'id'`), pero no sabrás en qué línea ni en qué archivo ocurrió.
*   **Solución:** Usa `logger.error("Mensaje", exc_info=True)` para guardar el stack trace completo.

## 3. Log Panic (Demasiado ruido)
*   **Error:** Hacer logs de nivel `INFO` para cosas que ocurren 10.000 veces por segundo.
*   **Consecuencia:** Saturación de disco, latencia de red y una factura de Cloud Logging de miles de euros.
*   **Solución:** Usa `DEBUG` para cosas repetitivas y asegúrate de que en producción el nivel sea `INFO` o superior.

## 4. Multiprocessing y Logs
*   **Error:** Usar un `FileHandler` estándar con varios procesos escribiendo al mismo archivo.
*   **Consecuencia:** Logs mezclados, líneas corruptas o fallos de escritura porque el archivo está bloqueado.
*   **Solución:** Usa `QueueHandler` o escribe cada proceso a un archivo diferente.

## 5. El "Log de la Mentira"
*   **Error:** `logger.info("Archivo procesado correctamente")` antes de haber comprobado realmente que se guardó en la base de datos.
*   **Solución:** Haz el log DESPUÉS de confirmar que la operación tuvo éxito.

## Resumen: Calidad sobre Cantidad
Un buen sistema de logs debe ser como un buen libro: fácil de leer, con el contexto necesario en cada capítulo y sin paja innecesaria que distraiga de la trama principal (tu aplicación).
