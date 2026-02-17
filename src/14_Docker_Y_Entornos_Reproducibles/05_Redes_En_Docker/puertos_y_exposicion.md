# Puertos y Exposición: Abriendo agujeros con seguridad

Exponer un puerto es decirle a Docker: "Permite que el tráfico del mundo exterior llegue a este contenedor". Es un paso crítico para la seguridad.

## 1. EXPOSE en el Dockerfile
`EXPOSE 8000`
- **Timo Senior:** Esta línea es puramente **documental**. No abre ningún puerto realmente. Solo sirve para que otros desarrolladores (y herramientas como Docker Compose) sepan en qué puerto escucha la App.

## 2. El comando de mapeo (-p)
`docker run -p 8080:8000 mi_imagen`
- **8080 (Host):** El puerto que abres en tu ordenador/servidor.
- **8000 (Container):** El puerto donde la App está realmente escuchando.
- El tráfico que llegue a tu PC por el 8080 se redirige mágicamente al 8000 del contenedor.

## 3. Mapeo a IP específica (Seguridad)
Por defecto, `-p 8080:8000` abre el puerto en **todas** tus interfaces (incluyendo el WiFi público de una cafetería).
- **Mejor:** `docker run -p 127.0.0.1:8080:8000 ...`
- Esto asegura que solo TÚ (desde tu propio PC) puedes entrar a ese puerto. Imprescindible para bases de datos o paneles de control internos.

## 4. Puertos Dinámicos (-P)
Si usas `-P` (mayúscula), Docker mapeará todos los puertos expuestos en el Dockerfile a puertos aleatorios de tu sistema operativo.
- **Uso:** Útil en tests automáticos para evitar conflictos de "Puerto ya en uso" si lanzas varios contenedores a la vez.

## 5. Escaneando puertos abiertos
Para saber qué está exponiendo realmente un contenedor:
```bash
docker port nombre_contenedor
```

## Resumen: Menos es Más
Expón solo lo estrictamente necesario. Si tu base de datos solo la usa tu API, **no mapees los puertos de la DB al host**. Deja que hablen por la red interna de Docker, manteniendo la base de datos totalmente invisible desde Internet.
