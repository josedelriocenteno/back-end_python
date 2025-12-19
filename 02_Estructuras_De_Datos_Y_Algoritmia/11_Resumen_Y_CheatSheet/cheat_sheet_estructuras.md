# Cheat Sheet – Estructuras de Datos en Python

| Estructura | Orden | Acceso | Inserción/Eliminación | Unicidad | Uso típico | Nota profesional |
|------------|-------|--------|---------------------|----------|------------|----------------|
| `list`     | Sí    | O(1) índice | append O(1), insert/pop O(n) | No       | Secuencias ordenadas, buffers pequeños | Evita pop(0) en listas grandes; usar deque si FIFO |
| `tuple`    | Sí    | O(1)   | Inmutable | Sí (hashable) | Retornos múltiples, claves dict | Inmutable → seguro y ligero |
| `set`      | No    | O(1)   | O(1)   | Sí       | Eliminación duplicados, membership test | No asumir orden, no almacenar mutables |
| `dict`     | No    | O(1)   | O(1)   | Claves únicas | Lookup rápido, cache, entidades | No claves mutables, cuidado con anidamiento profundo |
| `deque`    | Sí    | O(n)   | append/pop O(1) ambos extremos | No | FIFO, buffers, ventanas deslizantes | Mejor que list para colas largas |
| `stack` (list) | Sí | O(1) top | O(1) push/pop | No | Undo/Redo, backtracking | Siempre append/pop al final |
| `priority queue` (heapq) | Parcial | O(1) top | O(log n) | No | Scheduling, tasks con prioridad | No usar si solo FIFO es suficiente |
| `Counter` (collections) | N/A | O(1) | O(1) | Claves únicas | Conteos, histogramas | Más rápido que dict manual |
| `defaultdict` (collections) | N/A | O(1) | O(1) | Claves únicas | Inicialización automática, agrupaciones | Evita chequeos de existencia |
| `namedtuple` (collections) | Sí | O(1) | Inmutable | Sí (hashable) | Datos estructurados ligeros | Alternativa a clases simples |
| `ChainMap` (collections) | Parcial | O(1) | O(1) | Claves únicas | Composición de dicts | Útil para configuraciones, entornos múltiples |

## Reglas rápidas de decisión

1. **Necesito orden** → `list` o `tuple`
2. **Necesito acceso rápido por clave** → `dict`
3. **Necesito unicidad** → `set`
4. **FIFO real / ventana deslizante** → `deque`
5. **LIFO / pila** → `stack` con `list`
6. **Prioridades** → `heapq`
7. **Conteos frecuentes** → `Counter`
8. **Inicialización automática** → `defaultdict`
9. **Datos estructurados ligeros** → `namedtuple`
10. **Composición de dicts** → `ChainMap`

## Notas de backend/data engineering

- `list` → batches pequeños, acumuladores
- `set` → validación rápida de IDs/roles
- `dict` → modelado de entidades, cache
- `deque` → pipelines, buffers, ventanas temporales
- Cambiar estructura es más efectivo que optimizar microcódigo
- Siempre considerar Big-O en diseño antes de implementar
