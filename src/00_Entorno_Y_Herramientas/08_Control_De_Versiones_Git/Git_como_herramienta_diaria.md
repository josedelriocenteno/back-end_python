# Git como Herramienta Diaria para Backend Python

## 1. Introducción

Git no es solo para guardar código: es **la herramienta central de control y colaboración** en proyectos profesionales.  
Usarlo correctamente a diario permite **organizar, revisar y auditar cambios**, además de evitar errores y conflictos en equipo.

> ⚠️ Nota:
> Tratar Git como una herramienta estratégica, no solo como un repositorio de código, diferencia a un desarrollador junior de uno profesional.

---

## 2. Principios del uso diario

1. **Commit frecuente**: pequeños cambios que documentan evolución.  
2. **Actualización constante**: pull frecuente desde main o develop para evitar conflictos.  
3. **Branching disciplinado**: trabajar siempre en ramas feature/bugfix/hotfix.  
4. **Revisión de cambios antes de commit**: asegurar calidad y coherencia.  
5. **Automatización y hooks**: linters, tests y formateo automático antes de cada commit.

---

## 3. Comandos esenciales diarios

### 3.1 Estado y diferencias

```bash
git status          # Ver cambios locales
git diff            # Ver cambios sin añadir al staging
git diff --staged   # Ver cambios preparados para commit
3.2 Añadir y commitear
bash
Copiar código
git add app/main.py              # Añadir archivo específico
git add .                        # Añadir todos los cambios
git commit -m "feat(auth): JWT login"  # Commit semántico
3.3 Sincronizar con remoto
bash
Copiar código
git pull origin main            # Traer cambios de la rama principal
git push origin feature/login  # Subir cambios locales
3.4 Gestión de ramas
bash
Copiar código
git checkout -b feature/login  # Crear y cambiar a nueva rama
git branch                      # Listar ramas locales
git checkout main               # Cambiar a rama principal
git merge --no-ff feature/login # Merge profesional
4. Integración con flujo profesional
Pre-commit hooks: ejecutar linters y tests automáticamente:

bash
Copiar código
pip install pre-commit
pre-commit install
Trabajo en equipo: usar GitLab, GitHub o Bitbucket para PR y revisión.

Automatización de tareas: scripts que combinan Git + tests + despliegue:

bash
Copiar código
git pull origin main && pytest tests/ && git push origin feature/login
5. Buenas prácticas profesionales
Commits atómicos y semánticos: facilitan revisión y revert.

Actualizar la rama antes de trabajar: minimizar conflictos.

Evitar commits directos en main: usar PRs obligatoriamente.

Eliminar ramas antiguas: mantener repositorio limpio y organizado.

Documentar cambios importantes: commits y PR deben explicar “qué” y “por qué”.

6. Errores comunes a evitar
No hacer pull antes de empezar a trabajar.

Mezclar múltiples funcionalidades en un solo commit.

Ignorar conflictos y sobrescribir cambios de compañeros.

Trabajar directamente en main o develop.

No usar pre-commit hooks ni linters en commits diarios.

7. Checklist rápido
 Revisar estado con git status y diferencias con git diff

 Añadir cambios correctamente con git add

 Commit atómico y semántico

 Pull antes de iniciar cualquier trabajo

 Merge vía PR, con revisión y tests pasados

 Eliminar ramas locales/remotas innecesarias

 Usar pre-commit hooks para asegurar calidad diaria

8. Conclusión
Git debe ser una extensión diaria del flujo de trabajo profesional, no solo un repositorio.
Su uso disciplinado permite colaboración eficiente, trazabilidad completa y calidad constante en proyectos backend Python.
Adoptar esta mentalidad profesional distingue a un desarrollador junior de un profesional confiable.