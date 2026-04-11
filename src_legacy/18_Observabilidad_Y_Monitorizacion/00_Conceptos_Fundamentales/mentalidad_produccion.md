# Mentalidad de Producción: Pensar como un Ingeniero Senior

Un Ingeniero de Datos Senior no solo se preocupa de que el código funcione en su portátil, se preocupa de cómo va a sobrevivir el código en el "mundo cruel" de producción.

## 1. Asume que todo va a fallar
La red se caerá, el disco se llenará, y el proveedor de datos enviará basura.
*   **Mentalidad Senior:** "¿Cómo me entero de que esto ha fallado y qué información necesito para arreglarlo en 5 minutos?".

## 2. El Código es para humanos, los Logs para máquinas
Escribe código limpio, pero escribe logs estructurados. Un log que dice `"Error en el proceso"` no sirve de nada.
*   **Mejor:** `{"event": "db_connection_failed", "project": "ventas", "env": "prod", "reason": "timeout", "latency_ms": 5000}`.

## 3. Telemetría por diseño
No añadas la monitorización al final. El diseño de tus pipelines debe incluir puntos de medición desde el principio:
*   Contadores de filas procesadas.
*   Timers de cada fase (Extracción, Limpieza, Carga).
*   Validaciones de esquema automáticas.

## 4. No seas el "Hombre Alerta"
Si tu sistema envía 200 alertas al día, acabarás ignorándolas todas (**Alert Fatigue**). 
*   Configura alertas solo para cosas que requieran una acción humana inmediata.
*   El resto son métricas que se revisan en un dashboard semanal.

## 5. El Post-morten es sagrado
Cuando algo falla en producción y se arregla, el trabajo NO ha terminado.
*   ¿Por qué no lo detectamos antes?
*   ¿Qué métrica podríamos añadir para que la próxima vez el sistema nos avise antes del desastre?

## Resumen: Responsabilidad End-to-End
Tener mentalidad de producción significa ser responsable del dato desde que nace hasta que llega al usuario. La observabilidad es el lenguaje que usamos para comunicarnos con nuestro sistema y asegurar que cumple su misión.
