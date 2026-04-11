# Cobertura de Código y CI (Integración Continua)

Escribir tests es genial, pero asegurarte de que se ejecutan siempre y saber qué partes de tu código faltan por testear es lo que separa a un profesional de un amateur.

## 1. Cobertura de Código (Coverage)
La cobertura mide qué líneas de tu código han sido ejecutadas durante los tests.
*   **Herramienta:** `pytest-cov`.
*   **Ejecución:** `pytest --cov=app tests/`.
*   **El objetivo:** Apunta a un **80-90%**. Llegar al 100% suele ser muy caro y no siempre añade valor real, lo importante es testear la lógica de negocio crítica.

## 2. CI (Continuous Integration) con GitHub Actions
Tu código nunca debería entrar en la rama principal si los tests fallan. Configuramos un "Pipeline" que:
1.  Levanta un contenedor con Python.
2.  Instala las dependencias (`poetry install`).
3.  Levanta un contenedor de PostgreSQL (Service).
4.  Ejecuta los tests.

**Ejemplo de `main.yml`:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: |
          pip install pytest httpx fastapi
          pytest
```

## 3. Pruebas de Humo (Smoke Tests)
Son tests ultra-rápidos que solo verifican que los endpoints principales devuelven algo que no sea un error 500. Se lanzan justo después de un despliegue para asegurar que no hemos "quemado" el servidor.

## 4. Linting y Formateo (Flake8 / Black)
Aunque no son tests funcionales, aseguran que la calidad del código es consistente. Un fallo en el linter debe bloquear el despliegue igual que un test fallido.

## 5. El coste de los tests lentos
Si tu suite de tests tarda 20 minutos, los desarrolladores dejarán de correrla.
*   **Optimización:** Usa bases de datos en memoria para unit tests y agrupa los tests de integración pesados para que corran al final.

## Resumen: Calidad como Hábito
El testing no es una tarea que se hace al final; es parte del proceso de desarrollo. Una API testeada y con CI configurado es un activo valioso para la empresa. Una API sin tests es una responsabilidad peligrosa.
