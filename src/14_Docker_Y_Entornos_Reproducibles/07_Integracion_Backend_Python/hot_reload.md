# Hot Reload en Docker: Desarrollo sin esperas

En desarrollo, queremos que al guardar un archivo `.py`, el servidor se reinicie automáticamente dentro del contenedor. Esto requiere dos pasos clave.

## 1. El Bind Mount de Código
Debemos mapear nuestra carpeta local de desarrollo a la carpeta del contenedor.
```yaml
# En docker-compose.yml
services:
  web:
    volumes:
      - .:/app
```

## 2. El comando `--reload`
Uvicorn tiene un flag específico para monitorizar cambios.
```yaml
# En docker-compose.yml
services:
  web:
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 3. El problema de los permisos (Linux)
Si creas archivos desde dentro del contenedor (ej: con un generador de código), pertenecerán al usuario `root`.
- **Solución:** Configura tu usuario local en el Compose: `user: "1000:1000"`.

## 4. Consumo de CPU por Watcher
Monitorizar miles de archivos puede consumir mucha CPU.
- **Tip Senior:** Usa un archivo `.dockerignore` muy estricto para que el "watcher" no pierda tiempo mirando la carpeta `.git` o los `__pycache__`.

## 5. Hot Reload en Windows (WSL2)
A veces, los eventos del sistema de archivos no pasan bien de Windows a Linux.
- **Solución:** Asegúrate de que el código fuente esté DENTRO de la partición de WSL2 (ej: `\\wsl$\Ubuntu\home\user\code`), no en `C:\`.

## Resumen: Agilidad
Un entorno de desarrollo dockerizado solo es útil si no te frena. Configurar bien el volumes + reload es la diferencia entre amar Docker o odiarlo.
