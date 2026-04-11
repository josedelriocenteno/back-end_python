# Escaneo de Imágenes y Vulnerabilidades

Tu código puede estar perfecto, pero si la imagen base de Python que usas tiene una vulnerabilidad conocida en una librería de sistema antigua, tu servidor está en riesgo.

## 1. ¿Qué es el escaneo de imágenes?
Es una herramienta que analiza todos los archivos binarios y librerías dentro de tu imagen y los compara con bases de datos de vulnerabilidades públicas (**CVE - Common Vulnerabilities and Exposures**).

## 2. Herramientas recomendadas (Gratis y Pro)
- **Trivy:** La herramienta más popular y rápida actualmente.
- **Docker Scout:** Integrada directamente en el comando `docker`.
- **Snyk:** Muy centrada en el desarrollador, analiza también tu `requirements.txt`.

## 3. Ejemplo de escaneo con Docker
```bash
docker scout quickview mi_imagen:latest
docker scout cves mi_imagen:latest
```

## 4. Niveles de Gravedad
Las vulnerabilidades se clasifican en:
- **Low/Medium:** Riesgos teóricos o difíciles de explotar.
- **High/Critical:** ¡Peligro inminente! Debes actualizar la imagen base o la librería inmediatamente.

## 5. Integración en el Pipeline (CI/CD)
Un flujo de trabajo senior bloquea el despliegue si se detectan vulnerabilidades críticas.
```yaml
# Pseudo-código de GitHub Actions
- name: Scan Image
  run: trivy image --severity CRITICAL --exit-code 1 mi_imagen:latest
```
Si Trivy encuentra algo crítico, el script sale con error 1 y la App no llega a producción.

## Resumen: Confía pero verifica
El mundo de la seguridad cambia cada día. Escanear tus imágenes semanalmente te permite detectar fallos en librerías que ayer eran seguras pero hoy tienen un exploit público, permitiéndote reaccionar antes de que los atacantes lo hagan.
