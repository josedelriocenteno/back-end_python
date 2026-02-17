# Guía de Instalación de Docker

La instalación de Docker varía según tu sistema operativo, pero el objetivo es siempre el mismo: tener el **Docker Engine** y el **Docker Desktop** (opcional) listos para trabajar.

## 1. Linux (Recomendado para Backend)
En Linux es donde Docker "vive" de forma nativa. Se instala directamente en el kernel.
- **Ubuntu/Debian:** 
  ```bash
  sudo apt update
  sudo apt install docker.io docker-compose
  sudo usermod -aG docker $USER # Para correr docker sin 'sudo'
  ```
- **Ventaja:** Máximo rendimiento y compatibilidad total.

## 2. Docker Desktop (Windows / macOS)
En estos sistemas, Docker no puede correr nativamente, por lo que instala una micro-VM de Linux invisible para ejecutar los contenedores.
- **Instalación:** Descarga el instalador oficial desde [docker.com](https://www.docker.com/products/docker-desktop/).
- **Configuración:** Asegúrate de activar **WSL 2** en Windows para un rendimiento decente.
- **Ventaja:** Interfaz gráfica útil para monitorizar recursos y logs rápidamente.

## 3. Verificación de la instalación
Una vez instalado, abre tu terminal y ejecuta:
```bash
docker --version
docker compose version
docker run hello-world
```
Si ves el mensaje "Hello from Docker!", todo está configurado correctamente.

## 4. Recursos del sistema (⚠️ IMPORTANTE)
Docker Desktop puede consumir mucha RAM si no lo configuras.
- **Tip Senior:** Limita el uso de RAM y CPU en los ajustes de Docker Desktop (ej: 4GB de RAM y 2 nucleos) para que no bloquee tu IDE (VS Code o PyCharm).

## Resumen: Docker Engine vs Desktop
- **Docker Engine:** El motor central, gratuito y de código abierto.
- **Docker Desktop:** Una suite de herramientas gráficas propietaria. Imprescindible en Windows/Mac, opcional pero cómodo en Linux.
