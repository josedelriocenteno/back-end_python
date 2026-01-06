# code_smells.md

## Malos Olores de Código (Code Smells)

Los *code smells* son señales de que el código puede tener problemas de mantenimiento,
legibilidad o extensibilidad. No siempre son errores, pero **indican áreas que requieren refactorización**.

---

## 1️⃣ TIPOS COMUNES DE CODE SMELLS

### 1. Funciones gigantes (*Large Functions*)
- Funciones que hacen demasiadas cosas.
- Dificultan la lectura, prueba y refactorización.
- Señal de que deberías aplicar **SRP** y extraer funciones pequeñas.

**Ejemplo:**
```python
def procesar_pedido_completo(pedido: dict):
    # valida pedido
    # calcula total
    # aplica descuentos
    # guarda en DB
    # imprime resumen
    pass

Refactor sugerido: dividir en validar_pedido(), calcular_total(), aplicar_descuento(), etc.
2. Clases Dios (God Objects)

    Clases que contienen demasiadas responsabilidades.

    Mezclan lógica de negocio, persistencia e I/O.

    Difícil de mantener y testear.

Ejemplo:

class Pedido:
    # valida, calcula, aplica descuento, guarda, imprime
    pass

Refactor sugerido: aplicar SRP y dividir responsabilidades en varias clases pequeñas.
3. Código duplicado (Duplicated Code)

    Fragmentos repetidos en varios lugares.

    Incrementa errores y dificulta cambios futuros.

Solución: extraer funciones reutilizables, usar herencia o composición.
4. Condicionales complejas (Complex Conditionals)

    If/elif/else anidados o con lógica complicada.

    Difícil de leer y mantener.

Solución: usar guard clauses, dispatch dictionaries o Strategy Pattern.
5. Variables poco claras (Poor Naming)

    Nombres como a, b, x1, temp dificultan comprensión.

    Nombres claros = código auto-documentado.

6. Comentarios inútiles (Comments that lie or repeat)

    Comentarios que no aportan información adicional.

    Ejemplo: i = 0 # inicializa i a 0

    Mejor: código claro que se explique por sí mismo.

7. Código muerto (Dead Code)

    Funciones, clases o variables no usadas.

    Ocupan espacio y confunden.

    Herramientas: Flake8, Pylint detectan esto automáticamente.

8. Dependencias ocultas (Hidden Dependencies)

    Funciones o clases dependen de variables globales o estados implícitos.

    Dificultan pruebas y mantenimiento.

Solución: pasar dependencias explícitamente, usar inyección de dependencias.
9. Complejidad ciclomática alta (High Cyclomatic Complexity)

    Funciones con muchas ramas y loops.

    Difícil de testear y refactorizar.

Solución: dividir en funciones pequeñas, aplicar guard clauses, simplificar lógica.
🔟 Clases y funciones demasiado acopladas (Tightly Coupled Code)

    Cambiar una parte del código obliga a cambiar muchas otras.

    Dificulta mantenimiento y testing.

Solución: desacoplar usando interfaces, protocols, composition.
2️⃣ HERRAMIENTAS PARA DETECTAR CODE SMELLS
Herramienta	Qué detecta
Flake8	Estilo, variables no usadas, líneas largas
Pylint	Complejidad, docstrings faltantes, código muerto
McCabe	Complejidad ciclomática
mypy	Tipado y errores de tipo
Black	Formateo y consistencia (previene malos olores visuales)
3️⃣ PRINCIPIOS PARA REFRACTORIZAR CODE SMELLS

    Aplica SRP: cada función/clase = una sola responsabilidad.

    Extrae funciones y clases pequeñas.

    Usa guard clauses y patrones (Strategy, Repository).

    Elimina código duplicado y muerto.

    Mejora nombres de variables, funciones y clases.

    Centraliza dependencias y evita estados ocultos.

    Mantén complejidad baja.

    Asegura testabilidad.

4️⃣ CONCLUSIÓN

    Los code smells son alertas tempranas: no siempre errores, pero indican deuda técnica.

    Detectarlos y refactorizarlos mejora:

        Legibilidad

        Testabilidad

        Mantenibilidad

        Escalabilidad

    Combinando code smells con linters, formateadores y clean code, tu proyecto será profesional y preparado para producción.