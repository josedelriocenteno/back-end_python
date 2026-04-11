# Archivos que Nunca se Suben a Git para Backend Python

## 1. Introducción

No todos los archivos de un proyecto deben ser versionados.  
Subir archivos sensibles, temporales o generados automáticamente puede causar **problemas de seguridad, conflictos y desorden**.

> ⚠️ Nota:
> Mantener un `.gitignore` limpio y actualizado es **clave para proyectos profesionales**.

---

## 2. Tipos de archivos que nunca se deben subir

### 2.1 Archivos de configuración local

- `.env`, `.env.local` → Variables de entorno con contraseñas, tokens o claves API.  
- Configuraciones de IDE o editor local (`.vscode/`, `.idea/`).  
- Archivos de configuración personal (`config.json`, `settings_local.py`).

```gitignore
# Variables de entorno
.env
.env.local

# IDEs
.vscode/
.idea/
2.2 Archivos compilados o generados
Python: __pycache__/, .pyc, .pyo.

Carpeta de build o dist: build/, dist/, .egg-info/.

Logs generados automáticamente: logs/.

gitignore
Copiar código
# Python cache
__pycache__/
*.pyc
*.pyo

# Build
build/
dist/
*.egg-info

# Logs
logs/
*.log
2.3 Dependencias externas
Entornos virtuales completos: .venv/, venv/, env/.

Evitar subir librerías instaladas; usar requirements.txt o pyproject.toml.

gitignore
Copiar código
# Entornos virtuales
.venv/
venv/
env/
2.4 Archivos sensibles o secretos
Contraseñas, tokens, certificados (*.pem, *.key).

Datos de bases de datos locales (db.sqlite3).

gitignore
Copiar código
# Archivos sensibles
*.pem
*.key
db.sqlite3
2.5 Archivos temporales del sistema
Windows: Thumbs.db, Desktop.ini.

macOS: .DS_Store.

Linux: archivos de swap (*.swp, *~).

gitignore
Copiar código
# Sistema
Thumbs.db
Desktop.ini
.DS_Store
*.swp
*~
3. Buenas prácticas profesionales
Usar .gitignore desde el inicio del proyecto.

Revisar antes de cada commit: asegurarse que no se suben archivos sensibles.

Nunca versionar secretos ni claves de producción.

Usar herramientas de análisis de repositorios para detectar archivos sensibles accidentalmente.

Mantener consistencia en equipo: todos deben usar el mismo .gitignore.

4. Integración con flujo profesional
Crear .gitignore adaptado a Python y herramientas del proyecto:

bash
Copiar código
# Crear archivo .gitignore si no existe
touch .gitignore

# Agregar patrones recomendados
echo ".venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".env" >> .gitignore
Verificar cambios ignorados:

bash
Copiar código
git status --ignored
Nunca forzar un archivo ignorado con git add -f salvo casos excepcionales y documentados.

5. Errores comunes a evitar
Subir .env con credenciales reales.

Versionar carpetas de entornos virtuales completas.

No ignorar logs generados automáticamente.

Ignorar archivos temporales de sistema y editor.

Modificar .gitignore después de haber subido los archivos sensibles (requiere limpieza del historial con git rm --cached).

6. Checklist rápido
 .env y variables sensibles excluidas

 Entornos virtuales no versionados

 Carpeta __pycache__ y archivos .pyc ignorados

 Logs y archivos generados automáticamente ignorados

 Archivos temporales del sistema ignorados

 .gitignore revisado antes de cada commit

 Equipo siguiendo las mismas reglas de ignorar archivos

7. Conclusión
Mantener un .gitignore profesional evita problemas de seguridad, conflictos y desorden en proyectos backend Python.
Es un paso imprescindible desde el inicio del proyecto y debe formar parte de la cultura de trabajo en equipo.