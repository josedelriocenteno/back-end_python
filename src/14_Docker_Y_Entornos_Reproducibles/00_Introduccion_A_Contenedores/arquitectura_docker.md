# Arquitectura de Docker: Engine, Daemon y Cliente

Para diagnosticar problemas en Docker, primero hay que saber cómo se comunican sus piezas bajo el capó. No es una caja negra mágica; es una arquitectura Cliente-Servidor.

## 1. El Docker Demon (dockerd)
Es el "cerebro" que vive en el fondo de tu sistema operativo.
- Escucha las peticiones de la API de Docker.
- Gestiona los objetos: Imágenes, Contenedores, Redes y Volúmenes.
- Es el responsable real de que las cosas se ejecuten.

## 2. El Docker Client (CLI)
Es el comando `docker` que escribes en la terminal.
- No hace nada por sí solo. 
- Traduce tus comandos (ej: `docker run`) en llamadas a la API REST del demonio.
- El cliente y el demonio pueden estar en la misma máquina o en máquinas diferentes.

## 3. Docker Objects
- **Imágenes (Images):** Plantillas de solo lectura que contienen el código, librerías y configuración. Son como el "instalador" de un programa.
- **Contenedores (Containers):** Instancias ejecutables de una imagen. Es el proceso en ejecución.
- **Volúmenes (Volumes):** Donde vive la persistencia (archivos que no quieres que mueran cuando el contenedor pare).

## 4. Docker Registry (Docker Hub)
Es el "GitHub" de las imágenes.
- Cuando haces un `docker pull`, el Cliente le dice al Demonio que busque la imagen en un Registry (por defecto, Docker Hub).
- Puedes tener Registries privados en tu empresa (Amazon ECR, Google Artifact Registry).

## 5. Funcionamiento Interno (Namespaces y Cgroups)
Docker utiliza dos tecnologías clave del kernel de Linux:
1. **Namespaces:** Proporcionan aislamiento. El contenedor cree que tiene su propia red, su propio sistema de archivos y sus propios usuarios.
2. **Control Groups (cgroups):** Limitan los recursos. Evitan que un contenedor "se coma" toda la RAM o CPU del servidor físico, garantizando la convivencia de otros servicios.

## Resumen: Un sistema Modular
Cuando escribes `docker run hello-world`:
1. El **Cliente** envía la orden al **Demonio**.
2. El **Demonio** busca la imagen en el **Registry**.
3. El **Demonio** crea y lanza el **Contenedor** usando el kernel del SO.
