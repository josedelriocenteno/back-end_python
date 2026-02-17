# Tuning de Concurrencia: Ajustes en Producción

Tener el código correcto es el 50% del trabajo. El otro 50% es configurar el entorno de ejecución (servidor, uvicorn, worker pools) para que ese código rinda al máximo.

## 1. Uvicorn: Workers y Conexiones
Si usas FastAPI, `uvicorn` es tu motor.
- **Número de Workers:** `--workers 4`. Una regla de oro es `2 x (Suma_de_Nucleos) + 1`. Esto te da paralelismo a nivel de proceso (Multiprocessing) para manejar más peticiones.
- **Protocolo de Event Loop:** Usa `httptools` y `uvloop` (un event loop escrito en C que es mucho más rápido que el estándar de Python).

## 2. Ajustes del Sistema Operativo (Linux)
Cuando manejas miles de conexiones asíncronas, el SO puede bloquearte.
- **File Descriptors (`ulimit -n`):** Cada conexión de red es un archivo. Si el límite es 1024, tu App async no podrá manejar más de 1024 usuarios. Súbelo a 65535 en producción.
- **TCP Backlog:** El número de conexiones en espera de ser aceptadas.

## 3. Optimización del Recolector de Basura (GC)
En procesos asíncronos con mucha rotación de objetos pequeños, el GC de Python puede dispararse en momentos inoportunos.
- **Tip Senior:** Algunos desarrolladores desactivan el GC durante picos de tráfico y lo fuerzan manualmente en momentos de baja carga, aunque es una técnica avanzada y peligrosa.

## 4. Orquestación: Nginx como Escudo
Nunca expongas Uvicorn directamente a Internet. Usa **Nginx** por delante.
- Nginx gestiona mejor los "Slowloris" (ataques de conexiones lentas) y libera a tus workers de Python de tareas pesadas como servir archivos estáticos o comprimir con GZIP.

## 5. El coste del Context Switching
Si tienes 50 cores y lanzas 50 procesos, perfecto. Pero si lanzas 500 procesos, el microprocesador perderá más tiempo saltando de uno a otro que computando. Ajusta el número de procesos y hilos basándote en la carga real.

## Resumen: El Triángulo del Rendimiento
El rendimiento final depende de la **Eficiencia del Código** (algoritmos), la **Gestión de Recursos** (concurrencia) y la **Configuración del Entorno** (Tuning). Un administrador de sistemas senior sabe que no hay "balas de plata", solo ajustes finos basados en monitorización constante (Prometheus / Grafana).
