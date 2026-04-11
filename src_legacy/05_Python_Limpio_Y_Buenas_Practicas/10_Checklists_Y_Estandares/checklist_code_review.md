# checklist_code_review.md
===========================

Checklist: Qué revisar al hacer una code review profesional

Objetivo:
- Garantizar calidad y consistencia del código
- Evitar errores antes de mergear a main / producción
- Fomentar buenas prácticas y aprendizaje en equipo

---

## 1️⃣ ESTILO Y LEGIBILIDAD

- [ ] Código sigue PEP8 y guías internas de estilo
- [ ] Nombres de variables, funciones y clases claros y descriptivos
- [ ] Funciones pequeñas y enfocadas en una única responsabilidad
- [ ] Clases bien estructuradas, sin God Objects
- [ ] Comentarios y docstrings claros, necesarios y precisos
- [ ] Imports organizados y sin redundancias
- [ ] Longitud de líneas razonable (<88-100 caracteres)

---

## 2️⃣ TIPADO Y VALIDACIONES

- [ ] Type hints completos y correctos
- [ ] Validación de entradas y salidas donde corresponde
- [ ] Uso correcto de dataclasses, Value Objects o estructuras similares
- [ ] No usar `Any` a menos que sea necesario

---

## 3️⃣ CALIDAD Y COMPLEJIDAD

- [ ] Código modular y reutilizable
- [ ] Evitar condicionales anidados profundos (usar guard clauses)
- [ ] Evitar sobreingeniería y abstracciones innecesarias
- [ ] Funciones puras cuando sea posible, side effects controlados
- [ ] Uso correcto de patrones y buenas prácticas aprendidas

---

## 4️⃣ DEPENDENCIAS Y CONFIGURACIÓN

- [ ] Dependencias inyectadas explícitamente
- [ ] Configuración separada de código (env vars / settings)
- [ ] Revisar que no haya secretos o credenciales hardcodeadas
- [ ] Versionado de librerías correcto y coherente

---

## 5️⃣ TESTS Y REPRODUCIBILIDAD

- [ ] Test unitarios y de integración presentes y correctos
- [ ] Cobertura suficiente en funciones críticas
- [ ] Mocking correcto para dependencias externas
- [ ] Pipelines reproducibles, seeds fijadas en ML/Data
- [ ] Datos y modelos versionados cuando aplica

---

## 6️⃣ MANEJO DE ERRORES Y LOGGING

- [ ] Excepciones claras y controladas
- [ ] Logging consistente y sin prints casuales
- [ ] Manejo centralizado de errores donde aplica
- [ ] Comprobación de edge cases y errores comunes

---

## 7️⃣ DOCUMENTACIÓN Y COMENTARIOS

- [ ] README y documentación actualizada
- [ ] Comentarios claros donde el código no sea obvio
- [ ] Metadatos de experimentos, datasets o modelos (si aplica)
- [ ] Ejemplos de uso si aplica

---

## 8️⃣ PRUEBAS FINALES

- [ ] Código probado en entorno limpio
- [ ] Linter y formateador ejecutados
- [ ] Todos los tests pasados
- [ ] Revisar que no haya código muerto o redundante
- [ ] Confirmar que merge no romperá main / producción

---

## 9️⃣ CONCLUSIÓN

- Una **code review profesional** no solo busca errores, sino mejorar:
  - Legibilidad
  - Mantenibilidad
  - Reproducibilidad
  - Seguridad
  - Buenas prácticas del equipo

- Seguir esta checklist asegura código de calidad y reduce riesgos en producción.
