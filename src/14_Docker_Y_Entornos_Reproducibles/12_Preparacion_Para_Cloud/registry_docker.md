# Registry de Docker: Tu almacén de artefactos

Un **Docker Registry** es como un repositorio de Git, pero para imágenes binarias. Entender cómo gestionar el ciclo de vida de tus imágenes es vital para el equipo de DevOps.

## 1. Registries Públicos vs Privados
- **Públicos (Docker Hub):** Ideales para imágenes base o proyectos Open Source.
- **Privados (Amazon ECR, Google Artifact Registry):** Imprescindibles en empresa para que nadie fuera de la organización pueda descargar tu código propietario.

## 2. Flujo de Push/Pull
Para subir una imagen a un registro privado:
1. **Login:** `docker login <url_registro>`
2. **Tag:** `docker tag mi-app <url_registro>/mi-app:v1`
3. **Push:** `docker push <url_registro>/mi-app:v1`

## 3. Gestión de Costes y Espacio
Los registros de la nube cobran por GB almacenado.
- **Tip Senior:** Configura **Lifecycle Policies**. Por ejemplo: "Borrar automáticamente cualquier imagen que no se haya usado en 30 días o mantener solo las últimas 10 imágenes". Sin esto, la factura de AWS crecerá eternamente.

## 4. Escaneo Nativo
La mayoría de registros profesionales (ECR, GCR, Azure ACR) escanean automáticamente tus imágenes en busca de virus y vulnerabilidades en cuanto las subes.

## 5. Pull Secrets
Para que tu servidor de producción (o tu clúster de Kubernetes) pueda descargar la imagen del registro privado, necesita permisos. 
- No uses tu usuario/password personal. Usa **Service Accounts** o **IAM Roles** específicos para esta tarea.

## Resumen: El eslabón de la cadena
El Registry es la "fuente de la verdad". Cualquier imagen que esté ahí debe estar lista para producción. Trátalo con el mismo respeto y orden que tratas a tus ramas de Git.
