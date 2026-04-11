# Errores Comunes en Dockerfiles

Estos son los "miedos" clásicos que te harán perder horas si no los conoces de antemano.

## 1. Instalar dependencias innecesarias
Meter `vim`, `ping`, `curl` o herramientas de red en la imagen de producción. 
- **Problema:** Aumenta el peso y ayuda a los hackers si logran entrar al contenedor.
- **Solución:** Si necesitas debuggear, usa `docker exec` o imágenes de debug aparte.

## 2. No gestionar la caché de Pip
Si instalas librerías sin la opción `--no-cache-dir`, Pip guardará una copia de los instaladores dentro de la imagen.
- **Solución:** `pip install --no-cache-dir -r requirements.txt`.

## 3. Hardcodear secretos (Peligro Máximo)
Meter contraseñas de base de datos o API Keys en el `ENV` del Dockerfile.
- **Problema:** Cualquiera con acceso al `docker inspect` o a la imagen puede verlas. El historial de capas guarda el secreto para siempre.
- **Solución:** Usa variables de entorno (`.env`) al ejecutar el contenedor o servicios de secretos (Vault).

## 4. El error de `WORKDIR` relativo
Si no usas `WORKDIR`, el default es la raíz `/`. Si luego usas rutas relativas, puedes sobreescribir archivos críticos del sistema operativo accidentalmente.
- **Solución:** Establece siempre un `WORKDIR /app` al principio.

## 5. Confundir `ENTRYPOINT` con `CMD`
- `ENTRYPOINT`: Es el comando que NO se puede sobreescribir fácilmente al arrancar.
- `CMD`: Es el comando que se puede cambiar al vuelo (ej: `docker run mi_imagen bash`).
- **Error:** Usar `ENTRYPOINT` para algo que deberías cambiar habitualmente (ej: lanzar tests vs lanzar la app).

## 6. No limpiar el sistema de archivos tras el build
Dejar archivos temporales, carpetas de descarga o la caché de compilación.
- **Solución:** Borra todo en la misma línea del `RUN` que lo creó.

## Resumen: Limpieza y Discreción
Un buen Dockerfile es "mudo" (no expone secretos) y "limpio" (no deja rastro de su construcción). Si evitas estos fallos, tus despliegues serán mucho más profesionales y seguros.
