# Commits Limpios y Semánticos en Git para Backend Python

## 1. Introducción

Un commit limpio y semántico no solo guarda cambios, sino que **documenta la evolución del proyecto**, facilita la revisión y mejora la trazabilidad en equipo.  
Dominar esta práctica es **indispensable en entornos profesionales**.

> ⚠️ Nota:
> Los commits son historia del proyecto. Un mal commit puede generar confusión, errores y deuda técnica.

---

## 2. Principios de commits limpios

1. **Atómicos:** un commit = un cambio lógico.  
2. **Claridad:** mensaje claro que explique qué y por qué se hizo el cambio.  
3. **Consistencia:** seguir una convención semántica de mensajes.  
4. **Predecibles:** facilitan revertir, revisar y auditar cambios.  

---

## 3. Convención de commits semánticos

**Formato recomendado:**

```text
<tipo>[alcance opcional]: descripción breve
Tipos principales:
Tipo	Uso
feat:	Nueva funcionalidad
fix:	Corrección de bug
chore:	Tareas de mantenimiento (dependencias, scripts, etc.)
refactor:	Refactorización sin cambiar comportamiento
test:	Añadir o modificar tests
docs:	Cambios en documentación

Ejemplos prácticos:
bash
Copiar código
git commit -m "feat: agregar endpoint de login con JWT"
git commit -m "fix: corregir validación de email en registro"
git commit -m "refactor: separar lógica de autenticación en service"
git commit -m "test: agregar tests unitarios para endpoint login"
git commit -m "docs: actualizar README con instrucciones de setup"
💡 Tip:
Alcance opcional: permite indicar módulo o archivo afectado.
Ejemplo: feat(auth): agregar JWT para login

4. Buenas prácticas profesionales
Commits pequeños y enfocados

Evitar commits grandes con múltiples cambios no relacionados.

Mensaje en presente

Ejemplo correcto: feat: agregar endpoint

Incorrecto: agregué endpoint

Evitar commits vacíos

Solo agregar cambios con impacto real.

Revisar antes de commitear

git diff para ver los cambios que se están agregando.

Usar pre-commit hooks

Para linters, formateo automático y tests antes de commit.

5. Integración con flujo profesional
Crear rama específica para la funcionalidad o bug:

bash
Copiar código
git checkout -b feature/login
Hacer cambios atómicos y revisarlos:

bash
Copiar código
git add app/auth.py
git diff --staged
Commit semántico:

bash
Copiar código
git commit -m "feat(auth): agregar JWT para login"
Push y PR para revisión:

bash
Copiar código
git push origin feature/login
💡 Tip:
Mantener commits limpios facilita squash merge, revert y seguimiento de cambios en producción.

6. Errores comunes a evitar
Hacer commits gigantescos con múltiples funcionalidades.

Mensajes vagos o genéricos (arreglos, cambios, update).

Olvidar revisar cambios antes de commitear.

Mezclar código funcional con cambios de estilo o documentación en el mismo commit.

Ignorar pre-commit hooks y linters.

7. Checklist rápido
 Commit atómico por cada cambio lógico

 Mensaje claro y semántico

 Presente y conciso

 Revisar cambios con git diff antes de commitear

 Pre-commit hooks activos

 Commit enfocado en funcionalidad, bug, refactor, test o docs

 Facilita squash merge y revert si es necesario

8. Conclusión
Los commits limpios y semánticos son esenciales para mantener un historial claro, seguro y profesional en cualquier proyecto backend Python.
Seguir esta práctica mejora la colaboración en equipo, revisión de código y trazabilidad de cambios.