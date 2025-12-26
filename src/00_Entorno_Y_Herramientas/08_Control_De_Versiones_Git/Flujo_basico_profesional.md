# Flujo Básico Profesional de Git para Backend Python

## 1. Introducción

Git es la herramienta de control de versiones más usada en desarrollo profesional.  
Dominar un **flujo básico profesional** permite trabajar en equipo, mantener código limpio y evitar conflictos.

> ⚠️ Nota:
> No se trata solo de ejecutar comandos, sino de seguir un flujo **consistente y reproducible** en todos los proyectos.

---

## 2. Principios del flujo profesional

1. **Ramas separadas para cada funcionalidad** (`feature`), bug (`bugfix`) o hotfix (`hotfix`).  
2. **Commits pequeños y significativos** con mensajes claros y consistentes.  
3. **Integración continua en la rama principal** (`main` o `master`) solo después de revisión y tests.  
4. **Revisión de código obligatoria** mediante pull requests (PR).  
5. **Evitar commits directos a la rama principal** en proyectos profesionales.

---

## 3. Flujo básico recomendado

```text
main
  └─ feature/nueva-funcionalidad
      └─ bugfix/correccion-error
3.1 Crear rama para nueva funcionalidad
bash
Copiar código
# Asegurarse de estar en main y actualizado
git checkout main
git pull origin main

# Crear nueva rama para la funcionalidad
git checkout -b feature/login
3.2 Hacer cambios y commits limpios
bash
Copiar código
# Revisar cambios
git status

# Añadir cambios al staging
git add app/main.py

# Hacer commit con mensaje claro y semántico
git commit -m "feat: agregar endpoint de login con JWT"
💡 Tip:
Mensajes recomendados:

feat: nueva funcionalidad

fix: corrección de bug

chore: tareas internas, sin impacto en funcionalidad

refactor: refactorización de código

test: agregar o modificar tests

3.3 Sincronizar con remoto
bash
Copiar código
# Subir rama al repositorio remoto
git push origin feature/login
3.4 Pull Request y revisión
Abrir PR hacia main.

Solicitar revisión de compañeros o senior.

Integrar feedback antes de merge.

Asegurarse que tests pasen y linters estén limpios.

3.5 Merge profesional
bash
Copiar código
# Después de aprobar PR
git checkout main
git pull origin main
git merge --no-ff feature/login

# Subir cambios finales
git push origin main
⚠️ Nota:
--no-ff mantiene el historial de ramas, útil para trazabilidad profesional.

4. Buenas prácticas profesionales
Commits atómicos: un commit = un cambio lógico.

Mensajes claros y consistentes.

Actualizar rama antes de merge para evitar conflictos.

Evitar rebase en ramas compartidas sin coordinación.

Integrar pre-commit hooks para linters y formateo automático.

5. Errores comunes a evitar
Hacer commits grandes con múltiples cambios no relacionados.

Trabajar directamente en main sin revisión.

Ignorar conflictos y sobrescribir cambios de otros.

No usar mensajes claros y consistentes en commits.

Olvidar ejecutar linters y tests antes de mergear.

6. Checklist rápido
 Rama feature/bugfix creada para cada cambio

 Commits pequeños, claros y semánticos

 Pull request abierto y revisado

 Conflictos resueltos antes del merge

 Merge con --no-ff para mantener historial

 Tests y linters pasados antes de integrar cambios

7. Conclusión
Seguir un flujo básico profesional de Git asegura que el código se mantenga limpio, seguro y colaborativo.
Dominar este flujo es imprescindible para trabajar en empresas y proyectos reales de backend Python.