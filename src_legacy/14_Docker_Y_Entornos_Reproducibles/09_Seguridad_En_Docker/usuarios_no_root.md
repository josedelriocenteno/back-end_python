# Usuarios No-Root: Evitando la escalada de privilegios

Por defecto, Docker ejecuta tus aplicaciones con el usuario `root`. Esto significa que si un atacante logra explotar un bug en tu API de Python, tendrá control total sobre el contenedor y, potencialmente, sobre el servidor anfitrión.

## 1. Por qué es un peligro real
Si el contenedor corre como root y logran hackearlo, el atacante puede:
- Instalar herramientas de ataque (`nmap`, `netcat`).
- Acceder a otros contenedores en la misma red.
- Si hay un fallo de seguridad en el Kernel (Container Escape), podría convertirse en root de tu servidor real y borrarlo todo.

## 2. Implementación en el Dockerfile
Debemos crear un usuario sin privilegios y decirle a Docker que lo use.

```dockerfile
# 1. Creamos el usuario
RUN useradd -m -u 1000 myuser

# 2. Damos permisos a la carpeta de la App
RUN chown -R myuser:myuser /app

# 3. Cambiamos de usuario
USER myuser

# Todo lo que venga después corre como 'myuser'
CMD ["python", "main.py"]
```

## 3. Limitaciones del usuario No-Root
- No puedes usar puertos por debajo del 1024 (ej: el puerto 80).
- **Solución:** Escucha en el 8000 o el 8080 y usa el mapeo de Docker para sacarlo al 80 exterior.

## 4. Verificación de seguridad
Puedes comprobar qué usuario está corriendo realmente ejecutando:
```bash
docker exec nombre_contenedor whoami
```
Si el resultado es "root", tienes un problema de seguridad.

## 5. Imágenes base ya preparadas
Algunas imágenes (como `node` o `nginx`) ya traen un usuario no-root creado que solo tienes que activar con `USER node`. En la de Python, normalmente debes crearlo tú.

## Resumen: Principio de Menor Privilegio
Un profesional del backend nunca corre sus aplicaciones como root. Crear un usuario dedicado añade una capa de seguridad vital que puede salvarte de un desastre ante un bug imprevisto en tus dependencias.
