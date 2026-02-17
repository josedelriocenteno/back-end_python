# Gunicorn vs Uvicorn: Preparando Producción

En desarrollo usamos `uvicorn --reload`, pero en producción necesitamos algo mucho más robusto que aguante miles de peticiones reales.

## 1. Uvicorn (El Motor Async)
Uvicorn es extremadamente rápido pero es un servidor de un solo hilo. Si la CPU se bloquea, el servidor se detiene.

## 2. Gunicorn (El Manager de Procesos)
Gunicorn es un servidor "clásico" que sabe gestionar múltiples procesos (Workers). Se encarga de levantar nuevos workers si uno muere.

## 3. El Combo Ganador: Gunicorn + Uvicorn Workers
Usamos Gunicorn como "capitán" y le decimos que use la clase de worker de Uvicorn.
```bash
# Comando para el Dockerfile de Producción
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

## 4. ¿Cuántos Workers poner?
En Docker, la regla de `2 x Nucleos + 1` es relativa porque tú limitas la CPU del contenedor.
- **Tip Senior:** Si limitas tu contenedor a 1 CPU, poner 4 workers solo causará que peleen entre ellos. Pon 1 o 2 workers por contenedor y escala lanzando **más contenedores** (escalado horizontal).

## 5. El problema de los Timeouts
Si tu API hace tareas pesadas (ej: generar un PDF), Gunicorn matará el proceso si tarda más de 30s por defecto.
- **Solución:** Ajusta `--timeout 120` si esperas peticiones lentas, pero ten cuidado de no dejar recursos bloqueados.

## 6. Logs de Producción
Gunicorn permite separar los logs de acceso (quién entra) de los logs de error (qué falló).
- Configura `--access-logfile -` para que los logs salgan por la terminal y Docker los pueda capturar.

## Resumen: Estabilidad Industrial
No despliegues con `uvicorn` a secas. Usa `gunicorn` con la clase de worker de `uvicorn` para tener lo mejor de ambos mundos: la velocidad de la asincronía y la robustez de un gestor de procesos profesional.
