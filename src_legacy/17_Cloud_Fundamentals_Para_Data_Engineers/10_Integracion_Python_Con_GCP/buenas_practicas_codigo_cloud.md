# Buenas Prácticas de Código en la Nube

Escribir código para la nube es diferente a escribir código local. La red falla, el sistema externo puede ir lento y los costes cuentan. Sigue estas reglas de oro.

## 1. Reintentos (Retries) automáticos
Las librerías oficiales de Google ya traen reintentos para errores 500 (servidor), pero no para errores de tu propia lógica.
- **Tip:** Si tu script usa una API externa, usa librerías como `retrying` o `tenacity` para implementar Exponential Backoff.

## 2. Timeouts Estratégicos
Nunca dejes una conexión abierta indefinidamente. 
- Si BigQuery no ha respondido en 5 minutos, probablemente algo va mal. Configura un timeout para que el proceso "muera" y Airflow pueda volver a lanzarlo o avisarte.
```python
query_job = client.query(query, timeout=300) # 5 minutos
```

## 3. Logging Estructurado en Código
Usa el módulo `logging` de Python pero prepáralo para la nube.
- Incluye el `batch_id` en cada mensaje.
- Usa niveles correctos: `INFO` para flujo normal, `ERROR` solo cuando se requiere acción humana.
- Configura el formateador para que escriba en una sola línea (JSON).

## 4. Gestión de Conexiones (Pools)
Crear un cliente (`storage.Client()`) es una operación pesada.
- **BIEN:** Crea un único cliente al inicio de tu script y pásalo a las funciones.
- **MAL:** Crear un cliente nuevo dentro de un bucle que se repite 10.000 veces. Bloquearás el sistema y ralentizarás el proceso.

## 5. Stateless: Nada es para siempre
Asume que el disco duro de la máquina donde corre tu Python (Cloud Run o Function) va a borrarse en cuanto termine el script.
- Si guardas un archivo con resultados, súbelo a Cloud Storage. **Nunca** esperes encontrarlo ahí en la siguiente ejecución.

## 6. Manejo de Secretos (Secret Manager)
NUNCA uses variables de entorno para passwords si el entorno es compartido. Usa la librería de `google-cloud-secret-manager` para leer el secreto justo cuando lo vayas a usar.

## Resumen: Código Resiliente
Programar para la nube es programar para la incertidumbre. Un código profesional en GCP es aquel que asume que la red fallará, que protege sus secretos y que deja suficientes pistas (logs) para que el equipo pueda operarlo con seguridad.
