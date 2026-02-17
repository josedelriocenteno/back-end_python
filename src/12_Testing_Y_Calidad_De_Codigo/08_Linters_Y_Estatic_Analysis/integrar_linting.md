# Integración de Linting en el Flujo Local (Pre-commit)

Si dependes de que el desarrollador "se acuerde" de pasar el linter, fallarás. La solución es automatizarlo mediante **Pre-commit Hooks**.

## 1. ¿Qué es Pre-commit?
Es una herramienta que ejecuta scripts automáticamente cada vez que haces `git commit`. Si el código no pasa el linter, el commit falla y no se guarda.

## 2. Archivo `.pre-commit-config.yaml`
Este archivo define qué herramientas se ejecutan y en qué orden.
```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
```

## 3. Instalación
```bash
pip install pre-commit
pre-commit install  # Instala los hooks en tu carpeta .git/
```

## 4. Ventajas del Pre-commit
- **Código siempre limpio:** Es imposible subir código mal formateado al repositorio.
- **Pipelines más rápidas:** Si el fallo se detecta en local (en 1 segundo), no gastas minutos de servidor de CI/CD para enterarte.
- **Paz Mental:** El desarrollador se olvida del estilo y deja que la herramienta trabaje por él.

## 5. Ruff: El Futuro del Linting
Como desarrollador senior, debes conocer `Ruff`. Es un linter escrito en Rust que sustituye a Flake8, Isort y decenas de herramientas más siendo **100 veces más rápido**. Muchos proyectos modernos están migrando a Ruff para tener feedback instantáneo.

## Resumen: Automatizar o Morir
La calidad no puede ser una opción. Integrar el linting en el flujo de Git asegura que el estándar del equipo se respeta sin fricción y sin discusiones innecesarias.
