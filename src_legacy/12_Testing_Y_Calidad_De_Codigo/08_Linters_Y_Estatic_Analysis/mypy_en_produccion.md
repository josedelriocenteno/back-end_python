# Mypy: Tipado Estático en el Mundo Dinámico

Python es un lenguaje de tipado dinámico, pero desde la versión 3.5 podemos usar "Type Hints" (`def suma(a: int, b: int) -> int`). `Mypy` es la herramienta que comprueba estos tipos antes de ejecutar el código.

## 1. Por qué usar Mypy en Producción
- **Evita errores de 'NoneType':** Mypy te avisará si una función puede devolver `None` y no lo has manejado.
- **Documentación Garantizada:** Los tipos dicen exactamente qué espera una función sin necesidad de leer el cuerpo.
- **Refactorización Segura:** Si cambias el tipo que devuelve una función, Mypy marcará en rojo todos los sitios del proyecto que se han roto por ese cambio.

## 2. Configuración `pyproject.toml` o `setup.cfg`
Es vital configurar Mypy en modo estricto para que aporte valor real.
```ini
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true  # Obliga a poner tipos en todas las funciones
ignore_missing_imports = true # Para librerías viejas que no tienen tipos
```

## 3. Tipos Avanzados
Aprende a usar el módulo `typing`:
- `Optional[str]`: Puede ser un string o `None`.
- `Union[int, float]`: Acepta cualquiera de los dos.
- `Any`: Desactiva la comprobación (evítalo siempre que puedas).
- `Protocol`: Para definir interfaces estructurales.

## 4. Mypy y Pydantic
FastAPI y Pydantic funcionan de maravilla con Mypy. Existe un plugin de Pydantic para Mypy que ayuda a validar que estás pasando los datos correctos a tus modelos.

## 5. El coste de entrada
Añadir Mypy a un proyecto antiguo ("Legacy") puede ser muy duro (verás miles de errores).
- **Truco Senior:** Empieza con una configuración laxa e incrementa la restricción poco a poco. Usa `# type: ignore` solo para casos de vida o muerte donde la librería externa sea imposible de tipar.

## Resumen: La Seguridad de los Tipos
Mypy convierte a Python en un lenguaje mucho más cercano a Java o Go en cuanto a seguridad en tiempo de compilación. Elimina toda una categoría de bugs estúpidos y permite escalar bases de código a cientos de miles de líneas sin miedo.
