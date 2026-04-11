# Exec e Inspección: Entrando en la caja negra

A veces los logs no son suficientes y necesitas "entrar" al contenedor para ver qué está pasando con el sistema de archivos o la red.

## 1. Docker Exec: La terminal remota
`docker exec -it mi_app bash`
- Te abre una terminal dentro del contenedor. Puedes navegar por `/app`, ver variables de entorno con `env` o probar conexiones de red.
- **Tip Senior:** Si usas imágenes `alpine` o `slim`, puede que no tengan `bash`. Usa `sh` en su lugar.

## 2. Docker Inspect: La verdad del JSON
`docker inspect mi_app`
- Devuelve un objeto JSON gigante con TODA la configuración: redes, volúmenes, montajes, variables de entorno, ID del proceso real en el host, etc.
- **Uso útil:** `docker inspect -f '{{.NetworkSettings.IPAddress}}' mi_app` para sacar solo la IP interna.

## 3. Docker Stats: Monitorización en tiempo real
`docker stats`
- Muestra una tabla dinámica con el consumo de CPU, RAM y Red de todos tus contenedores.
- Es el `top` de Docker. Úsalo para detectar fugas de memoria (Memory Leaks) en tu App de Python.

## 4. Docker Top
`docker top mi_app`
- Muestra los procesos de Linux que están corriendo DENTRO del contenedor vistos desde el HOST.
- Ayuda a ver si tu App ha lanzado subprocesos inesperados (ej: procesos zombie).

## 5. Ver el sistema de ficheros (`docker diff`)
`docker diff mi_app`
- Muestra qué archivos han sido creados (A), modificados (C) o borrados (D) desde que el contenedor arrancó respecto a la imagen original.
- **Uso:** Perfecto para ver si tu App está escribiendo basura en carpetas que no debería.

## Resumen: Herramientas de diagnóstico
`logs` para saber qué dice la App, `stats` para saber cómo está de salud y `exec` para operar quirúrgicamente sobre ella. Aprender estos comandos te salvará de horas de incertidumbre ante fallos extraños.
