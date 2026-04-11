# Pylint: Análisis Profundo de Código

Mientras que Flake8 se centra en el estilo, `Pylint` es un linter mucho más sofisticado que analiza la "salud" de tu código: detecta variables no usadas, código inalcanzable, lógica duplicada y mucho más.

## 1. Ejecución y Puntuación
Al ejecutar `pylint src`, la herramienta te dará una nota del 1 al 10.
- Un proyecto senior debería aspirar siempre a una nota > 9.0.

## 2. Archivo `.pylintrc`
Pylint es muy estricto por defecto. Necesitas un archivo de configuración para desactivar avisos que no tengan sentido en tu entorno (ej: quejas sobre nombres de variables cortos en matemáticas).
```bash
pylint --generate-rcfile > .pylintrc
```

## 3. Qué detecta Pylint que otros no ven
- **Variables no utilizadas:** Evita dejar basura en el código.
- **Código Inalcanzable:** Detecta `return` prematuros o `if` que siempre son `False`.
- **Similaridades:** Detecta bloques de código casi idénticos (Copy-Paste).
- **Consistencia de Nombres:** Asegura que las clases son CamelCase y las funciones snake_case.

## 4. Refactorización Sugerida
Si tienes una clase con demasiados métodos (Too many public methods) o demasiados atributos, Pylint te avisará. Es una señal directa de que estás violando el **Principio de Responsabilidad Única**.

## 5. Integración con el IDE
Pylint puede ser lento en proyectos grandes. La mayoría de desarrolladores senior lo configuran para que se ejecute solo al guardar archivos específicos en el editor o como un paso previo al commit.

## Resumen: El Auditor de Código
Pylint es como tener un desarrollador senior revisando cada línea de tu código en tiempo real. Puede ser frustrante al principio por su rigor, pero a largo plazo te enseña a escribir un código mucho más limpio y robusto.
