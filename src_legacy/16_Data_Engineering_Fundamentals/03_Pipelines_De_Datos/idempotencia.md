# Idempotencia: El pilar de la fiabilidad

La **Idempotencia** es la propiedad de una operación que, sin importar cuántas veces se ejecute, siempre produce el mismo resultado final sin causar efectos secundarios duplicados.

## 1. Por qué es vital en Data Engineering
Los pipelines fallan. Si tu pipeline inserta ventas y falla a mitad, cuando lo reinicies:
- **Sin idempotencia:** Insertarás las ventas de nuevo y los números estarán duplicados.
- **Con idempotencia:** El sistema detectará que esas ventas ya existen y solo insertará lo que falte o sobreescribirá lo anterior sin duplicar.

## 2. Estrategias de Idempotencia
- **Overwrite (Sobreescritura):** "Borra la partición del 15 de Mayo y escríbela de nuevo". Si se ejecuta 10 veces, el resultado es el mismo.
- **Upsert (Update + Insert):** Basado en una clave primaria (ID). Si el registro existe, se actualiza; si no, se inserta.
- **Deduplicación:** Un paso al final del pipeline que limpia registros idénticos antes de darlos por buenos.

## 3. El concepto de "Deterministic Processing"
Para que un pipeline sea idempotente, debe ser determinista: con el mismo input, siempre debe generar el mismo output. Evita funciones como `random()` o usar la hora actual `now()` dentro de la lógica principal si eso afecta al resultado del dato.

## 4. Diseño de "At Least Once"
La mayoría de sistemas de datos garantizan la entrega "Al menos una vez" (At least once). Esto significa que el dato llegará SÍ O SÍ, pero puede llegar duplicado. La idempotencia es tu defensa contra esos duplicados del sistema.

## 5. Tip Senior: Falla con elegancia
Diseña tus pipelines pensando en que se van a re-ejecutar. Si tu código asume que la carpeta de destino siempre está vacía, no es idempotente. Tu código debe ser capaz de "limpiar la casa" antes de empezar a trabajar.

## Resumen: Robustez Matemática
La idempotencia es lo que te permite dormir tranquilo. Sabes que si un proceso falla a las 3 AM, el reintento automático no va a "romper los números" del negocio.
