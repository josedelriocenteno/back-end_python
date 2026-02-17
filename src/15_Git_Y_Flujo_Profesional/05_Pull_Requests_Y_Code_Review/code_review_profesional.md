# Code Review Profesional: Crítica constructiva

Revisar código es tan importante como escribirlo. Un buen revisor detecta bugs, malas prácticas y mejora la coherencia de todo el proyecto.

## 1. ¿Qué NO es una Code Review?
- No es una competición de egos.
- No es para buscar culpables.
- No es para discutir sobre preferencias estéticas (para eso están los Linters).

## 2. Qué mirar (Prioridades)
1. **Lógica y Bugs:** ¿Hace lo que dice que hace? ¿Hay casos borde (nulls, errores de red) no controlados?
2. **Diseño y Arquitectura:** ¿Sigue los patrones del proyecto? ¿Es extensible?
3. **Mantenibilidad:** ¿Es fácil de leer? ¿Los nombres de variables son descriptivos?
4. **Seguridad:** ¿Hay secretos hardcodeados? ¿Validación de inputs?

## 3. Cómo dar Feedback (Seniors)
- **Sé amable:** Usa "Podríamos" en vez de "Deberías". "Me pregunto si..." en vez de "Esto está mal".
- **Explica el PORQUÉ:** No digas "Usa un set aquí". Di "Usa un set aquí para que la búsqueda sea O(1) en lugar de O(n)".
- **Propón soluciones:** Si algo está mal, ofrece un snippet de código como alternativa.
- **Distingue importancia:** Usa etiquetas como `[NIT]` (Nitpick) para sugerencias menores que no deben bloquear el merge.

## 4. El "Good Enough"
No busques la perfección eterna. Si el código es correcto, seguro y mejor de lo que había, **apruébalo**. No bloquees el trabajo de un compañero por una preferencia subjetiva.

## 5. Elogios (Approve with Praise)
Si ves una solución brillante o un código muy limpio, **dilo**. Las Code Reviews también sirven para motivar y celebrar el buen trabajo.

## Resumen: Responsabilidad Compartida
Cuando apruebas una PR, te conviertes en co-autor de ese código. Si falla en producción, es responsabilidad de ambos. Revisa con cuidado, pero siempre con respeto y mentalidad de equipo.
