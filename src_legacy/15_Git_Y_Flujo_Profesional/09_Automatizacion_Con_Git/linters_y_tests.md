# Linters y Tests: Calidad Automática

No confíes en tu memoria. Configura herramientas que verifiquen tu código cada vez que intentes guardarlo en Git.

## 1. ¿Qué es un Linter?
Es una herramienta que analiza tu código estáticamente (sin ejecutarlo) buscando errores potenciales o fallos de estilo.
- **Python:** `Flake8` (estilo), `Pylint` (lógica y calidad), `Mypy` (tipos).

## 2. ¿Qué es un Formateador?
A diferencia del linter (que solo avisa), el formateador cambia tu código para que siga un estándar.
- **Python:** `Black` es el estándar de facto. "The uncompromising code formatter".

## 3. Integración en el Flujo de Git
La mejor forma de usarlos es mediante un hook de **pre-commit**.
```yaml
# Ejemplo de .pre-commit-config.yaml
repos:
-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
```

## 4. Tests Unitarios en el Commit
Si tus tests son rápidos (milisegundos), añádelos al pre-commit.
- Si un cambio rompe un test existente, Git no te dejará hacer el commit. Esto previene que subas código roto al servidor.

## 5. El coste de la automatización
Al principio puede ser frustrante que Git te "prohíba" hacer commit por un espacio de más. Pero a largo plazo, ahorra cientos de horas de depuración y discusiones en las Pull Requests.

## Resumen: Estándar y Disciplina
La automatización eleva el nivel de todo el equipo. No importa quién escriba el código, gracias a los linters y formateadores, todo el proyecto parecerá escrito por la misma persona.
