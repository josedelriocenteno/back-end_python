# configuracion_proyecto.md

## Centralizando la configuración del proyecto con `pyproject.toml`

`pyproject.toml` es el estándar moderno para configurar herramientas de Python
(linters, formateadores, type checkers) en un solo lugar. Esto evita tener múltiples
archivos de configuración y asegura que todo el equipo siga las mismas reglas.

---

## 1️⃣ ESTRUCTURA BÁSICA DEL ARCHIVO

```toml
[tool.black]
line-length = 88
target-version = ["py39"]
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
combine_as_imports = true
known_first_party = ["myproject"]
known_third_party = ["numpy", "pandas", "django"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
skip = [".venv", "build", "dist"]

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
exclude = [".git", "__pycache__", "venv"]

[tool.pylint.'MESSAGES CONTROL']
disable = ["C0114", "C0115", "C0116"]

2️⃣ EXPLICACIÓN DETALLADA
Black

    line-length = 88: compatible con PEP8 y legibilidad

    target-version: define versión Python para compatibilidad

    include / exclude: qué archivos se formatean y qué carpetas se ignoran

Isort

    profile = "black": compatibilidad con Black

    sections: separa imports por tipo

    known_first_party / known_third_party: ayuda a clasificar imports locales vs terceros

    multi_line_output, include_trailing_comma, combine_as_imports: formatea automáticamente imports largos o múltiples

Flake8

    max-line-length = 88: asegura coherencia con Black

    extend-ignore: ignora ciertas reglas conflictivas con Black

    exclude: carpetas a ignorar

Pylint

    'MESSAGES CONTROL': permite deshabilitar mensajes opcionales

    Ideal para evitar falsos positivos si ya usamos docstrings según otra convención

3️⃣ BENEFICIOS DE CENTRALIZAR CONFIGURACIÓN

    Todo el proyecto sigue las mismas reglas de estilo y calidad.

    Evita conflictos entre herramientas (Black, Flake8, Isort).

    Facilita integración con CI/CD y pre-commit hooks.

    Mantiene consistencia en equipos grandes.

    Facilita onboarding de nuevos desarrolladores.

4️⃣ INTEGRACIÓN CON PRE-COMMIT

Archivo .pre-commit-config.yaml recomendado:

repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8

  - repo: https://github.com/PyCQA/pylint
    rev: v2.17.0
    hooks:
      - id: pylint

    Al hacer commit, pre-commit ejecutará todas las herramientas usando la configuración centralizada.

    Garantiza que todo el código que entra al repositorio cumple las mismas reglas.

5️⃣ REGLAS DE ORO

    Nunca mezcles configuraciones en múltiples archivos si puedes centralizar.

    Mantén el pyproject.toml en la raíz del proyecto.

    Usa versiones fijas de herramientas para evitar cambios inesperados.

    Combina con pre-commit para revisión automática y uniforme.

    Revisa periódicamente las reglas y ajusta según evolución del proyecto.

6️⃣ CONCLUSIÓN

pyproject.toml centraliza y unifica:

    Formateo automático (Black)

    Orden de imports (Isort)

    Linting y chequeo de estilo (Flake8, Pylint)

Esto asegura que tu proyecto sea:

    Limpio

    Profesional

    Mantenible

    Escalable