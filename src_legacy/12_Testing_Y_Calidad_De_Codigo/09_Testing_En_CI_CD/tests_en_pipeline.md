# Automatización de Tests en la Pipeline de CI/CD

El CI (Continuous Integration) es el proceso de integrar cambios de código de forma frecuente en una rama principal, disparando una serie de pruebas automáticas. Si los tests fallan, el código no se integra.

## 1. El Flujo Estándar
Cada vez que haces un `git push`, el servidor de CI (GitHub Actions, GitLab CI, Jenkins) hace lo siguiente:
1. **Prepare Environment:** Monta un servidor virtual limpio con Python.
2. **Install Dependencies:** Instala tus librerías (`pip install -r requirements.txt`).
3. **Static Analysis:** Ejecuta Linters (Flake8) y MyPy.
4. **Unit Tests:** Ejecuta Pytest y genera el reporte de cobertura.
5. **Integration Tests:** Levanta servicios temporales (DB, Redis) y prueba la conexión real.

## 2. Ejemplo de GitHub Actions (`.github/workflows/tests.yml`)
```yaml
name: Python Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run Pytest
      run: pytest --cov=src --cov-report=xml
```

## 3. Caché de Dependencias
Instalar librerías en cada ejecución es lento.
- **Tip Senior:** Usa la acción de caché de GitHub para guardar la carpeta de `pip`. Esto puede reducir el tiempo de la pipeline de 5 minutos a 1 minuto.

## 4. Estrategia de Entornos (Environment Isolation)
La pipeline debe ser capaz de recrear un entorno idéntico al de producción.
- Usa **Docker Compose** dentro de la pipeline para levantar la base de datos real.
- Usa variables de entorno (`ENV`) para configurar los punteros a los servicios de test.

## 5. Artifacts (Artefactos)
Si un test falla, quieres ver por qué.
- Configura la pipeline para "subir" (upload) el reporte HTML de cobertura o los logs de error como artefactos. Así puedes descargarlos y analizarlos desde la web de GitHub.

## Resumen: La Pipeline no miente
Un backend profesional nunca confía en el "en mi máquina funciona". La pipeline de CI es el juez final y objetivo. Mantenerla rápida y fiable es una de las tareas más importantes de un desarrollador senior.
