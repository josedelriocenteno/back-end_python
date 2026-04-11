# Versionado Semántico (SemVer): El lenguaje de las versiones

¿Cómo decidimos si nuestra App pasa de la `1.4.2` a la `1.5.0` o a la `2.0.0`? El estándar **SemVer** responde a esto de forma lógica.

## 1. La estructura `X.Y.Z`
- **X (MAJOR):** Cambios que rompen la compatibilidad (Breaking changes). Requieren que el usuario cambie su código para seguir usando tu API.
- **Y (MINOR):** Nuevas funcionalidades que no rompen nada (Backward-compatible).
- **Z (PATCH):** Corrección de bugs (Backward-compatible).

## 2. Etiquetas de Git (Git Tags)
Las versiones se marcan en Git usando tags.
- `git tag -a v1.0.0 -m "Primera versión estable"`
- `git push origin v1.0.0`
- **Tip:** Al subir tags, GitHub/GitLab suelen crear automáticamente una "Release" descargable con el código en ese estado.

## 3. Automatización con Conventional Commits
Aquí es donde todo encaja. Si usas Conventional Commits, herramientas como **Semantic Release** pueden:
1. Leer tus mensajes de commit desde la última versión.
2. Detectar si hay `feat:` (sube MINOR) o `fix:` (sube PATCH).
3. Buscar `!` o `BREAKING CHANGE` (sube MAJOR).
4. Crear el tag y subirlo sin intervención humana.

## 4. Versiones de Desarrollo
- `1.0.0-alpha`: Versión muy inestable, solo para pruebas internas.
- `1.0.0-beta`: Funcionalidades completas pero con bugs conocidos.
- `1.0.0-rc` (Release Candidate): Lista para producción si no surgen sustos de última hora.

## 5. Calendar Versioning (CalVer)
Algunos proyectos (como Ubuntu o PyCharm) usan el año y el mes: `v2024.1`. Útil para software que se actualiza por fecha y no por saltos de funcionalidad.

## Resumen: Predictibilidad
El versionado semántico da seguridad a tus usuarios. Saben que si actualizan un parche (`Z`), nada se romperá. Si actualizan una versión mayor (`X`), deben tener cuidado. Es el contrato de confianza entre el desarrollador y el usuario.
