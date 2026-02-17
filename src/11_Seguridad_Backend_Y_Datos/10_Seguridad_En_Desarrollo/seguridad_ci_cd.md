# Seguridad en CI/CD: La Pipeline de Confianza

Tu pipeline de CI/CD (GitHub Actions, GitLab CI, Jenkins) es el motor que lleva tu código a producción. Si la pipeline no es segura, todo lo demás da igual.

## 1. El Concepto de "Gatekeeping" de Seguridad
La pipeline debe actuar como un guardia: si los tests de seguridad no pasan, el despliegue se cancela automáticamente.
- **Fase 1 (Commit):** Linting y SAST (Bandit).
- **Fase 2 (Build):** Escaneo de dependencias (Safety/Snyk).
- **Fase 3 (Alpha/Staging):** DAST (Dynamic Testing) y Tests de Integración de seguridad.

## 2. Gestión de Secretos en la Pipeline
- **NUNCA:** Poner secretos en el archivo `.yaml` de la pipeline.
- **SIEMPRE:** Usar "Secrets" de GitHub o GitLab. Estas variables se inyectan en memoria y se ocultan de los logs de la ejecución de la pipeline (aparecen como `***`).

## 3. Seguridad de las Imágenes de Docker
Si despliegas con contenedores:
- Escanea la imagen base en busca de vulnerabilidades (`docker scan` o herramientas como Trivy).
- No corras el contenedor como `root`. Crea un usuario `appuser` dentro del Dockerfile.

## 4. Despliegues Inmutables
Una vez que una versión se despliega, no se debe entrar al servidor a "tocar nada" manualmente por SSH. Si hay un parche de seguridad, se hace un nuevo despliegue desde la pipeline. Esto asegura que lo que hay en producción es trazable y reproducible.

## 5. Auditoría de la Pipeline
¿Quién puede cambiar la pipeline? ¿Quién puede disparar un despliegue a producción? Usa **Branch Protection** para que nadie pueda subir código directamente a `main` sin un Code Review y sin que pasen todos los checks de seguridad.

## Resumen: Automatizar para no fallar
La seguridad manual es un mito. Los humanos nos cansamos y nos saltamos pasos. Una pipeline de CI/CD con seguridad integrada garantiza que cada línea de código que llega a tus usuarios ha pasado por un riguroso examen de calidad y blindaje.
