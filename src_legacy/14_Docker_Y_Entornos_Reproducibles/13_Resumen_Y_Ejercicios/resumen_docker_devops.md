# Resumen Maestro: Docker & DevOps para Backend

Docker no es una herramienta opcional en 2024; es el idioma universal de la infraestructura moderna. Aquí tienes los pilares fundamentales para un desarrollador senior.

## 1. El Concepto: Inmutabilidad y Aislamiento
- Las imágenes no se editan, se **reconstruyen**.
- Los contenedores son procesos, no máquinas virtuales.
- Si algo falla: `kill -> rebuild -> run`. No arregles cosas "en caliente".

## 2. Dockerfile: El Arte de la Optimización
- Usa **Multi-stage builds** para separar el entorno de compilación del de ejecución.
- Prefiere versiones **slim** sobre las completas.
- El orden de los comandos importa para el **caching** de capas.

## 3. Docker Compose: Orquestación Local
- Centraliza toda tu infraestructura (App + DB + Redis).
- Usa **nombres de servicios** para que se vean entre sí.
- Protege los datos con **volúmenes** nombrados.

## 4. Seguridad: El Escudo Invisible
- Nunca corras aplicaciones como **Root**.
- No metas secretos en las imágenes (usa `.env` o Vault).
- Escanea tus imágenes buscando vulnerabilidades (Trivy).

## 5. El Salto a Cloud
- Diseña pensando que el disco local es efímero.
- Saca la base de datos a un servicio gestionado.
- Usa registros privados y etiquetas inmutables (Commit SHA).

## Checklist del Desarrollador Senior
1. [ ] ¿Mi imagen es pequeña (<200MB)?
2. [ ] ¿Pasa el escaneo de seguridad sin fallos críticos?
3. [ ] ¿Usa un usuario no-root?
4. [ ] ¿Tiene un Healthcheck definido?
5. [ ] ¿Los logs salen por stdout en formato JSON?

---
Docker es la base sobre la que se construye el escalado horizontal y la alta disponibilidad. Dominar estos conceptos te permite dejar de preocuparte por "la máquina" y centrarte en el valor de tu código y tus datos.
