# Configuración de Cobertura con coverage.py

La cobertura de código (Code Coverage) es una métrica que indica qué porcentaje de tus líneas de código han sido ejecutadas durante los tests. La herramienta estándar para esto en Python es `coverage.py` (o su plugin `pytest-cov`).

## 1. Instalación y Ejecución Básica
```bash
pip install pytest-cov
pytest --cov=src # Ejecuta tests y muestra cobertura de la carpeta src
```

## 2. Archivo de Configuración `.coveragerc`
No quieres medir la cobertura de todo. Debes ignorar carpetas de sistema, virtual environments y los propios tests.
```ini
[run]
source = src
omit =
    src/migrations/*
    src/tests/*
    */__init__.py

[report]
show_missing = True
exclude_lines =
    pragma: no cover
    def __repr__
    if __name__ == .__main__.:
    raise NotImplementedError
```

## 3. Pragma: no cover
A veces hay líneas de código que son imposibles de testear o que no aportan valor (ej: un `if` que solo se activa ante un fallo catastrófico del hardware).
- Usa el comentario `# pragma: no cover` para decirle a la herramienta que ignore esa línea en el cálculo del porcentaje. Úsalo con **extrema moderación**.

## 4. Tipos de Cobertura
- **Line Coverage:** ¿Se ejecutó esta línea?
- **Branch Coverage:** ¿Se probaron todos los caminos de un `if`? (Tanto el `True` como el `False`). Actívalo con `--cov-branch`. Es una métrica mucho más honesta.

## 5. Reportes HTML
Ver el resumen en la terminal está bien, pero para debuguear huecos de test, usa:
```bash
pytest --cov=src --cov-report=html
```
Esto genera una carpeta `htmlcov/` donde puedes abrir un `index.html` y ver, línea por línea en color rojo, qué partes de tu código no tienen test.

## Resumen: Una herramienta, no un objetivo
La cobertura es una brújula para encontrar sitios donde te has olvidado de testear. Un 90% de cobertura es genial, pero no sirve de nada si el 10% restante es el core de tu sistema de pagos.
