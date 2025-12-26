# VSCode: Configuración Profesional para Backend Python

## 1. Introducción

Visual Studio Code (VSCode) es uno de los editores más usados en desarrollo Python backend.  
Tener una **configuración profesional** optimiza productividad, reduce errores y facilita colaboración en equipo.

> ⚠️ Nota:
> Una mala configuración puede ralentizar el desarrollo y generar errores difíciles de depurar.

---

## 2. Instalación y configuración inicial

### 2.1 Instalación de VSCode
- Descargar desde [https://code.visualstudio.com/](https://code.visualstudio.com/)  
- Instalar versiones estables (LTS si disponible)

### 2.2 Configuración básica

```json
// settings.json
{
    "python.pythonPath": ".venv/bin/python",
    "editor.formatOnSave": true,
    "editor.tabSize": 4,
    "files.exclude": {
        "**/__pycache__": true,
        "**/.venv": true
    },
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.analysis.typeCheckingMode": "strict",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false
}
💡 Tip:
Configurar el path del intérprete Python al entorno virtual evita errores al instalar paquetes y correr scripts.

3. Extensiones imprescindibles
Extensión	Función
Python	Soporte de linting, debugging y testing
Pylance	Autocompletado avanzado y análisis de tipos
isort	Ordena importaciones automáticamente
Black	Formateador de código Python
GitLens	Control avanzado de Git y visualización de cambios
Docker	Integración con contenedores y Dockerfiles
Markdown All in One	Mejora el trabajo con documentación Markdown
Test Explorer UI	Gestión visual de tests

4. Configuración del depurador (Debugger)
4.1 Archivo launch.json
json
Copiar código
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload"
            ],
            "jinja": true
        }
    ]
}
Permite depurar la aplicación FastAPI directamente desde VSCode.

Incluye breakpoints, inspección de variables y ejecución paso a paso.

5. Snippets y atajos
Configurar snippets personalizados para CRUD, logging y tests acelera el desarrollo.

Atajos útiles:

Ctrl + Shift + P: abrir paleta de comandos

Ctrl + /: comentar/descomentar líneas

F5: iniciar depuración

Shift + Alt + F: formatear código con Black

6. Integración con Git
VSCode permite hacer commits, pull, push y revisar cambios directamente.

Configurar linters y formateo automático en cada commit con pre-commit hooks asegura calidad de código.

bash
Copiar código
# Ejemplo pre-commit
pip install pre-commit
pre-commit install
Hooks típicos:

Formateo con Black

Ordenación de imports con isort

Linting con Flake8

Type checking con Mypy

7. Buenas prácticas profesionales
Siempre usar entorno virtual y configurarlo en VSCode.

Formatear código automáticamente al guardar (formatOnSave).

Activar linting y type checking estrictos.

Configurar debugger para pruebas locales rápidas.

Integrar Git y pre-commit hooks para mantener calidad de código.

Mantener settings y extensiones documentadas en el proyecto.

8. Errores comunes a evitar
No usar entorno virtual dentro de VSCode (provoca paquetes faltantes).

Ignorar linters y type checkers.

No configurar debugger, lo que dificulta depuración.

Mezclar settings personales con configuraciones del proyecto.

No usar pre-commit hooks en equipo, generando inconsistencias de estilo.

9. Checklist rápido
 Entorno virtual configurado en VSCode

 Formateo automático y linting habilitados

 Depurador configurado para FastAPI

 Extensiones esenciales instaladas

 Integración con Git y pre-commit hooks activa

 Snippets y atajos configurados para productividad

10. Conclusión
Configurar VSCode de manera profesional aumenta productividad, previene errores y mejora la calidad del código.
Es fundamental para cualquier desarrollador backend que busque trabajar al nivel de empresas de primer nivel.