# Changelog: El historial para humanos

Mientras que los commits son para desarrolladores, el **CHANGELOG** es para los usuarios, los jefes de producto y otros equipos que usan tu software.

## 1. ¿Qué es un Changelog?
Es un archivo (normalmente `CHANGELOG.md`) que resume los cambios más importantes de cada versión de forma legible. No es un volcado de `git log`.

## 2. Secciones Estándar
- **Added:** Funcionalidades nuevas.
- **Changed:** Cambios en comportamiento existente.
- **Deprecated:** Funciones que se borrarán pronto.
- **Removed:** Funciones eliminadas.
- **Fixed:** Bugs corregidos.
- **Security:** Vulnerabilidades cerradas.

## 3. Keep a Changelog (El estándar)
Sigue estas reglas para un changelog profesional:
- Los cambios más recientes van arriba.
- Cada versión debe incluir la fecha de lanzamiento.
- Enlaza los diffs de GitHub entre versiones si es posible.

## 4. Generación Automática
No lo escribas a mano. Usa herramientas como **standard-version** o **conventional-changelog**.
- Leen tus commits semánticos.
- Agrupan por `feat`, `fix`, etc.
- Generan el archivo markdown perfecto en un segundo.

## 5. Por qué es importante
Cuando una librería que usas se actualiza y algo deja de funcionar, lo primero que haces es mirar su Changelog. Dale ese mismo respeto a tus propios usuarios.

## Resumen: Transparencia y Orden
Un buen Changelog ahorra cientos de preguntas tipo "¿qué hay de nuevo en esta versión?". Es el documento de "Gritos y Susurros" que mantiene a todos informados sobre la evolución del producto.
