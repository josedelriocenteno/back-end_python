# Partition Pruning: El súper-poder de las particiones

El **Partition Pruning** (Poda de Particiones) es la técnica por la cual el motor de la base de datos ignora por completo las particiones que sabe que no contienen los datos que buscas.

## 1. ¿Cómo funciona?
Imagina que tienes 12 particiones, una por mes.
```sql
SELECT * FROM ventas WHERE fecha >= '2024-03-01' AND fecha <= '2024-03-31';
```
Sin pruning, el motor miraría las 12 particiones. Con pruning activo, el optimizador dice: "Solo necesito la partición de Marzo, las otras 11 las ignoro".
*   **Resultado:** La query tarda 1/12 parte del tiempo.

## 2. Requisitos para el Pruning
Para que el pruning ocurra, se deben cumplir dos reglas:
1.  **Usar la clave de partición:** Debes incluir la columna por la que particionaste en tu cláusula `WHERE`.
2.  **Valores constantes o deterministas:** `fecha = '2024-01-01'` permite el pruning. `fecha = random_date()` a menudo NO lo permite porque el motor no puede predecir qué partición tocará antes de ejecutarla.

## 3. Pruning en Tiempo Real (Runtime Pruning)
A veces, el valor del filtro viene de otra tabla.
```sql
SELECT * FROM ventas v 
JOIN promociones p ON v.fecha = p.fecha_inicio
WHERE p.id = 50;
```
En este caso, el motor identifica durante la ejecución qué partición de `ventas` abrir basándose en el resultado de la tabla `promociones`. Sigue siendo muy eficiente.

## 4. Verificación con EXPLAIN
Puedes ver si el pruning está funcionando mirando el plan de ejecución.
*   **MAL:** Verás menciones a todas tus sub-tablas (`facturas_2021`, `facturas_2022`, etc).
*   **BIEN:** Solo verás que el motor accede a la partición específica que necesitas.

## 5. El impacto en índices locales
Cada partición tiene sus propios índices. El pruning no solo evita leer datos, evita tener que cargar y buscar en los índices de las particiones irrelevantes, ahorrando toneladas de memoria RAM y tiempo de CPU.

## Resumen: Eficiencia por Exclusión
El pruning es el motivo principal por el cual particionamos a gran escala. Es la capacidad de buscar en un pajar enorme mirando solo la esquina donde sabemos que está la aguja, descartando el resto del pajar de forma instantánea y automática.
