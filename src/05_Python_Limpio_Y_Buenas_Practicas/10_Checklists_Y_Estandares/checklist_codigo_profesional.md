# checklist_codigo_profesional.md
==================================

Checklist: Antes de entregar código

Objetivo:
- Asegurar que el código cumpla estándares profesionales
- Facilitar revisión y mantenimiento
- Evitar errores comunes en producción

---

## 1️⃣ ESTILO Y FORMATO

- [ ] Código sigue **PEP8** o guías de estilo del equipo
- [ ] Nombres de variables, funciones y clases **claros y descriptivos**
- [ ] Longitud de líneas < 88-100 caracteres (según estándar)
- [ ] Espacios, indentación y saltos de línea correctos
- [ ] Imports organizados y limpios (usar `isort` o similar)
- [ ] Docstrings presentes en funciones y clases públicas
- [ ] Comentarios claros y necesarios (sin redundancia)

---

## 2️⃣ TIPADO Y VALIDACIONES

- [ ] Tipado estático con **type hints** completo
- [ ] Validación de inputs y outputs donde sea necesario
- [ ] Uso de `dataclasses` o Value Objects para estructuras de datos
- [ ] Evitar `Any` a menos que sea estrictamente necesario

---

## 3️⃣ CALIDAD Y COMPLEJIDAD

- [ ] Funciones pequeñas: **una función = una responsabilidad**
- [ ] Evitar condicionales anidados profundos (usar guard clauses)
- [ ] Código modular y reutilizable
- [ ] Aplicación de **SOLID** y principios de clean code
- [ ] No hay funciones o clases “dios” (God Objects)
- [ ] No hay sobreingeniería ni abstracciones innecesarias

---

## 4️⃣ DEPENDENCIAS Y CONFIGURACIÓN

- [ ] Dependencias inyectadas explícitamente (no “magia”)
- [ ] Configuración separada de código (`settings`, variables de entorno)
- [ ] Versionado correcto de librerías críticas
- [ ] Entorno reproducible (requirements.txt, pyproject.toml, Poetry, etc.)

---

## 5️⃣ TESTS Y REPRODUCIBILIDAD

- [ ] Tests unitarios y de integración cubren el código principal
- [ ] Tests con **mocks** para dependencias externas
- [ ] Pipelines de datos / ML reproducibles y puros
- [ ] Random seeds fijadas para experimentos de ML
- [ ] Datos y modelos versionados si es necesario

---

## 6️⃣ MANEJO DE ERRORES Y LOGGING

- [ ] Excepciones controladas y significativas
- [ ] Logging consistente en lugar de prints casuales
- [ ] Manejo de errores centralizado cuando aplica
- [ ] No hay errores silenciosos o swallow exceptions

---

## 7️⃣ DOCUMENTACIÓN Y COMENTARIOS

- [ ] README actualizado y claro
- [ ] Documentación de módulos, funciones y clases
- [ ] Ejemplos de uso incluidos cuando aplica
- [ ] Changelog de cambios importantes

---

## 8️⃣ SEGURIDAD Y BUENAS PRÁCTICAS

- [ ] No exponer secretos en el código
- [ ] Revisar inyecciones o vulnerabilidades (SQL, OS, etc.)
- [ ] Validaciones de datos externas a la lógica
- [ ] Dependencias revisadas y actualizadas

---

## 9️⃣ REVISION FINAL

- [ ] Ejecutar **linter y formateador** (flake8, pylint, black)
- [ ] Ejecutar tests y pipelines completos
- [ ] Confirmar que todo funciona en entorno limpio
- [ ] Código listo para revisión por pares / code review
