# Aprobar y Rechazar: Decisiones Técnicas

Al final de una revisión, debes tomar una decisión. GitHub te da tres opciones principales, y saber cuál elegir es clave para el flujo del equipo.

## 1. Approve (Aprobar)
Significa: "Confío en este código y creo que está listo para producción".
- Solo aprueba cuando estés convencido de que no hay riesgos críticos.
- Puedes aprobar incluso con pequeños comentarios ("NITs") si confías en que el autor los corregirá antes de mergear.

## 2. Request Changes (Solicitar Cambios)
Significa: "Este código tiene problemas que DEBEN arreglarse antes de mergear".
- Úsalo para errores de lógica, fallos de seguridad o arquitectura que rompa el estándar.
- **⚠️ Importante:** Bloquea el botón de Merge para todos los demás. Úsalo con respeto y solo por causas justificadas.

## 3. Comment (Comentar)
Significa: "Tengo dudas o sugerencias pero no quiero bloquear el proceso todavía".
- Úsalo para pedir aclaraciones sobre por qué se tomó una decisión.
- Muy útil cuando eres nuevo en el proyecto y quieres aprender el contexto.

## 4. Resolver Conversaciones
Cuando el autor hace los cambios, se deben marcar las conversaciones como **Resolved**. Esto limpia la interfaz y ayuda a enfocar en lo que falta por revisar.

## 5. El conflicto de opiniones
¿Qué pasa si el autor y el revisor no se ponen de acuerdo?
1. **Charla directa:** Sal de GitHub y habla por Slack o en persona. 5 minutos de charla resuelven 2 días de hilos de comentarios.
2. **Third party:** Pide opinión a un tercer desarrollador (Senior/Lead) que actúe como mediador.

## Resumen: Flujo sin bloqueos
El objetivo no es ser un "portero" estricto, sino un facilitador. Busca siempre el equilibrio entre la calidad técnica y la velocidad de entrega del equipo.
