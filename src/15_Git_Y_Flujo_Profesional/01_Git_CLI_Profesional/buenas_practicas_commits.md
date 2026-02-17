# Buenas Prácticas en Mensajes de Commit

Un commit es una carta a tu "yo" del futuro y a tus compañeros de equipo. Escribir mensajes mediocres ralentiza a todo el equipo.

## 1. La Regla de Oro
**Un mensaje de commit debe explicar el PORQUÉ del cambio, no el QUÉ.** El "qué" ya está en el código (el diff).

## 2. El Imperativo
Usa verbos en imperativo: "Añadir", "Arreglar", "Cambiar". 
- **MAL:** `Arreglé el bug de login`
- **BIEN:** `Arreglar bug de login en dispositivos iOS`

## 3. La Estructura Profesional
1. **Línea de resumen:** Máximo 50 caracteres. Capitalizada. Sin punto al final.
2. **Línea en blanco.**
3. **Cuerpo del mensaje:** Explicación detallada si es necesario. Máximo 72 caracteres por línea.

## 4. Conventional Commits (Introducción rápida)
Usa prefijos para que el historial sea escaneable:
- `feat:` Funcionalidad nueva.
- `fix:` Corrección de error.
- `docs:` Cambios en documentación.
- `style:` Formato, puntos y coma (no lógica).
- `refactor:` Mejora de código sin cambiar comportamiento.

## 5. El Commit Atómico
No mezcles cosas. 
- **Error:** Un commit que actualiza el README, arregla el CSS y añade una tabla a la base de datos.
- **Solución:** Haz 3 commits pequeños. Es mucho más fácil hacer un "revert" de un commit pequeño si algo falla que de uno gigante.

## Resumen: Calidad desde la base
Los mensajes de commit demuestran tu nivel de profesionalismo. Si tus mensajes son claros y descriptivos, te ganarás el respeto de tus compañeros desde el primer día.
