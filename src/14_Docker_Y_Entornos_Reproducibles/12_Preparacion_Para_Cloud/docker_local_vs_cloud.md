# Docker Local vs. Cloud: El choque con la realidad

Lo que funciona perfectamente en tu ordenador con `docker compose up` puede fallar catastróficamente al desplegarlo en la nube (AWS, Google Cloud, Azure). Estas son las diferencias clave que debes conocer.

## 1. El mito del sistema de archivos local
- **Local:** Puedes usar Bind Mounts al disco de tu ordenador.
- **Cloud:** Los servidores son efímeros. Si escribes un archivo en el disco local de la instancia, **desaparecerá** cuando la nube decida reiniciar tu contenedor por mantenimiento.
- **Solución:** Usa servicios de almacenamiento gestionado (S3, Google Cloud Storage) o volúmenes de red (EFS, Azure Files).

## 2. Redes y Load Balancers
- **Local:** Expones un puerto (`-p 80:8000`) y ya está.
- **Cloud:** Docker suele correr detrás de un **Load Balancer (ALB / Cloud Run)**. No mapeas puertos manualmente; el orquestador gestiona el tráfico y tú solo le dices en qué puerto escucha tu contenedor internamente.

## 3. La Base de Datos ya no es un contenedor
- **Local:** Corres Postgres en un contenedor para mayor comodidad.
- **Cloud:** Correr bases de datos en contenedores en producción es muy complejo de gestionar. 
- **Solución:** Usa servicios gestionados (**RDS**, **Cloud SQL**). Tu contenedor Docker debe conectarse a estos servicios externos mediante variables de entorno.

## 4. Recursos limitados y agresivos
- **Local:** Docker usa toda la RAM disponible si no le pones límites.
- **Cloud:** Las nubes tienen sistemas de monitoreo muy estrictos. Si tu contenedor se pasa de la memoria asignada un solo byte, será aniquilado inmediatamente (OOMKill).
- **Tip Senior:** Configura siempre los `requests` y `limits` de memoria de forma conservadora.

## 5. Arquitectura de CPU (ARM vs x86)
- **Local:** Quizás usas un Mac con chip M1/M2/M3 (arquitectura ARM).
- **Cloud:** Muchos servidores antiguos o baratos usan Intel/AMD (x86).
- **Peligro:** Si compilas la imagen en ARM y la subes a un servidor x86, no funcionará. 
- **Solución:** Build multiplataforma con `docker buildx build --platform linux/amd64`.

## Resumen: Pensar en Distribuido
Pasar a la nube implica aceptar que tu contenedor es un grano de arena en el desierto. Diseña aplicaciones "Stateless" (sin estado local), centraliza los logs en la nube y asume que cualquier recurso que no sea computación pura (CPU) debe ser externo al contenedor.
