# Quality Gates: El Muro de Contención

Un **Quality Gate** (Puerta de Calidad) es un criterio automático que decide si el código puede ser integrado o si debe ser rechazado. No se trata de "pasar los tests", se trata de cumplir un estándar de calidad mínimo.

## 1. Cobertura Mínima Garantizada
Puedes configurar tu pipeline para que falle si la cobertura baja de un porcentaje (ej: 80%).
```bash
pytest --cov=src --cov-fail-under=80
```
- **Tip Senior:** Esto evita que el equipo "olvide" testear nuevas funcionalidades. Si añades 500 líneas de código sin test, la media bajará y la pipeline se pondrá roja.

## 2. Cero Errores de Tipado (Mypy)
Mypy en la pipeline asegura que ningún desarrollador se salta las reglas de tipos. Es un Quality Gate que previene errores de ejecución en producción de forma muy eficaz.

## 3. Sin Vulnerabilidades de Seguridad (SCA)
Configura escaneos de dependencias (`safety` o `snyk`) como un Quality Gate. Si se detecta que estás usando una librería con un hack conocido, el despliegue se bloquea.

## 4. Complejidad Ciclomática Controlada
Usa herramientas para bloquear el commit si alguna función supera una complejidad determinada (ej: > 15). Esto obliga al desarrollador a refactorizar antes de intentar integrar.

## 5. SonarQube y el "New Code"
Herramientas como SonarQube permiten distinguir entre:
- **Código Antiguo:** Puede tener deuda técnica (se perdona).
- **Código Nuevo:** Debe tener 0 errores, 0 vulnerabilidades y 80% de cobertura.
Esta estrategia permite mejorar gradualmente un proyecto "Legacy" sin obligar a testear todo lo viejo de golpe.

## Resumen: Automatizar la Exigencia
Los Quality Gates eliminan la subjetividad y la necesidad de "vigilar" a otros desarrolladores. El sistema es el que exige la calidad. Un backend profesional ve estas "puertas" no como un obstáculo, sino como la garantía de que su código vivirá en un entorno sano y estable.
