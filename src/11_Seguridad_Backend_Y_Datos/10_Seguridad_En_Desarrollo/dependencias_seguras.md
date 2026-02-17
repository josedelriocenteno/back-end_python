# Gestión de Dependencias Seguras (SCA)

Una aplicación backend moderna rara vez es código 100% propio. Usamos cientos de librerías externas. La **Seguridad en Dependencias (Software Composition Analysis)** consiste en asegurar que esas piezas de código de terceros no introducen vulnerabilidades en nuestro sistema.

## 1. El Riesgo de la Cadena de Suministro (Supply Chain)
- **Vulnerabilidades Conocidas (CVE):** Una versión antigua de Django o FastAPI puede tener un fallo que permita rce (Remote Code Execution).
- **Typosquatting:** Alguien publica una librería llamada `pandass` (con dos s) que es idéntica a `pandas` pero roba tus variables de entorno.
- **Librerías Abandonadas:** Si usas un paquete que no se actualiza hace 3 años, es probable que contenga bugs de seguridad no parcheados.

## 2. Herramientas de Escaneo en Python
No revises las librerías a mano. Usa automatización:
- **Safety:** Escanea tu `requirements.txt` o `pyproject.toml` en busca de vulnerabilidades conocidas.
- **Pip-audit:** Una herramienta más moderna y rápida que usa la base de datos de PyPI.
- **Snyk:** El estándar profesional. Analiza dependencias, licencias y código propio.

## 3. Versionado y "Pinning"
- **Mal:** `fastapi = "*"` (Instala siempre la última, puede romper tu código).
- **Bien:** `fastapi == 0.104.1`.
- **Mejor (Pinning):** Usa un archivo de bloqueo (`requirements.txt` generado por `pip freeze` o `poetry.lock`). Esto garantiza que lo que testeaste en local es exactamente lo mismo que se despliega en producción.

## 4. Actualización Responsable
No actualices por actualizar, pero tampoco dejes pasar meses.
- **Herramienta:** `Dependabot` (GitHub) o `Renovate`. Te abren un Pull Request cada vez que sale una versión nueva de una librería que usas, avisándote si tiene parches de seguridad.

## 5. Licencias Masivas
La seguridad también es legal. Escanear licencias asegura que no estás usando una librería que te obligue a hacer tu código fuente público (ej: licencias GPL en un proyecto comercial cerrado).

## Resumen: No confíes en extraños
Cada vez que haces `pip install`, estás metiendo el código de un desconocido en tu servidor de producción con todos tus secretos. Sé extremadamente selectivo con las librerías que usas y manténlas siempre vigiladas con escaneos automáticos.
