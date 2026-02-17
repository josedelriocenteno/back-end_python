# Límites del Backend: Concurrencia y Bloqueos

Incluso con los mejores servidores, un backend tiene límites físicos y lógicos que pueden bloquearlo. Estos son los "muros" contra los que chocarás.

## 1. Límite de Conexiones a la DB
Este es el fallo nº 1 en escalabilidad.
*   Si tu backend intenta abrir una conexión nueva para cada petición y tienes 1.000 peticiones por segundo, la base de datos se colapsará.
*   **Solución:** Usa un **Connection Pool** (visto en el Tema 06). Una "piscina" de conexiones abiertas que se reutilizan constantemente.

## 2. El GIL de Python
Como vimos, Python no puede ejecutar código en varios núcleos en el mismo proceso.
*   Si tu API hace cálculos pesados de forma síncrona, bloqueará todas las demás peticiones mientras termina.
*   **Solución:** Usa `asyncio` para I/O y `Gunicorn` o `Uvicorn` con múltiples Workers (procesos) para aprovechar todos los núcleos.

## 3. Límite de Archivos Abiertos (File Descriptors)
Cada conexión de red y cada archivo abierto en Linux cuenta como un "File Descriptor". El sistema operativo tiene un límite (`ulimit`).
*   Si tu API tiene muchas conexiones abiertas, puedes alcanzar el límite y empezar a rechazar nuevos usuarios con el error "Too many open files".

## 4. El "Bloqueo por Red"
Si tu API tiene que descargar una imagen de 100MB de otro sitio antes de responder al usuario, el hilo de ejecución estará bloqueado durante segundos.
*   **Solución:** Realiza estas tareas pesadas en segundo plano usando una cola de tareas como **Celery** o **Redis Queue**.

## 5. El coste de la Serialización JSON
En APIs de alto tráfico que mueven JSONs gigantes, el simple hecho de transformar el objeto Python a String (JSON) consume mucha CPU.
*   **Optimización:** Usa librerías ultra-rápidas como `ujson` u `orjson` en lugar del `json` estándar para ganar un 20% de rendimiento gratis.

## Resumen: Conoce tus debilidades
Escalar no es solo añadir servidores, es quitar los tapones que impiden que los datos fluyan. Entender cómo gestiona tu backend las conexiones, los hilos y los recursos del sistema operativo te permitirá construir servicios que no solo sean rápidos, sino que no se rompan ante una carga masiva.
