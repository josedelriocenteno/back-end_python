# Checklists de Review: Tu guía de calidad

Para no olvidar nada importante, los desarrolladores senior siguen una lista mental (o escrita) durante la revisión. Aquí tienes una lista de verificación universal.

## 1. Integridad y Lógica
- [ ] ¿El código hace exactamente lo que pide la tarea?
- [ ] ¿Hay lógica redundante o código muerto?
- [ ] ¿Se han tenido en cuenta los casos de error (excepciones)?

## 2. API y Contratos
- [ ] ¿Se han actualizado los tipos (Type Hints) correctamente?
- [ ] ¿El esquema de respuesta de la API ha cambiado de forma que rompa el Frontend?
- [ ] ¿Se han añadido los parámetros necesarios a la documentación?

## 3. Infraestructura y Datos
- [ ] ¿Hay migraciones de base de datos pendientes?
- [ ] ¿El cambio afecta al rendimiento de una query SQL?
- [ ] ¿Se han actualizado las variables de entorno necesarias?

## 4. Calidad y Style
- [ ] ¿Los nombres de las funciones son verbos y los de variables son sustantivos claros?
- [ ] ¿Las funciones son demasiado largas (>30-40 líneas)?
- [ ] ¿Faltan docstrings o comentarios en partes complejas?

## 5. Testing
- [ ] ¿El autor ha añadido tests unitarios para la nueva lógica?
- [ ] ¿Los tests pasan en el servidor de CI?
- [ ] ¿Se están testeando tanto los casos de éxito como los de fallo?

## Resumen: El estándar del equipo
Cada equipo suele tener su propia checklist adaptada a su lenguaje y framework. Úsala para ser consistente y asegurar que, pase quien pase la revisión, el nivel de calidad del proyecto siempre sea excelente.
