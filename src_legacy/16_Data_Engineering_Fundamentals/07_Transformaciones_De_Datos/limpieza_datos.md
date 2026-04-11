# Limpieza de Datos: La cura contra el ruido

La limpieza (Data Cleaning) es el conjunto de transformaciones necesarias para que el dato sea interpretable y consistente. Es la fase más pesada del ingeniero de datos.

## 1. Normalización de Textos
- **Case Formatting:** Convertir todo a minúsculas o mayúsculas para que la búsqueda sea consistente (`"España"` == `"españa"`).
- **Trimming:** Eliminar espacios en blanco invisibles al principio y al final del texto.
- **Sustitución:** Cambiar `"N/A"`, `"None"`, `"NULL"` por un valor nulo real o un valor por defecto.

## 2. Estandarización de Formatos
- **Fechas:** El estándar de oro es **ISO 8601** (`YYYY-MM-DDTHH:MM:SSZ`). Nunca guardes fechas en formatos locales.
- **Monedas:** Convertir todo a una moneda base (ej: USD o EUR) usando el tipo de cambio del día.
- **Unidades:** Convertir metros a kilómetros, libras a kilos, etc.

## 3. Manejo de Nulos (Imputación)
¿Qué hacemos cuando falta un dato?
- **Descarte:** Ignorar la fila (solo si no es crítica).
- **Default:** Poner un valor por defecto (ej: `País = "Desconocido"`).
- **Media/Mediana:** Rellenar con el promedio estadístico (común en ML).

## 4. Tipado Correcto (Casting)
A veces el CSV dice que el precio es `"10.50"` (Texto). Debes convertirlo a `Float` o `Decimal` para poder sumarlo.
- **Tip Senior:** Usa `Decimal` para dinero. Evita `Float` por los problemas de precisión de redondeo.

## 5. El criterio de "Limpieza Extrema"
No limpies lo que no necesites. Cada transformación consume CPU y dinero. Si una columna no se va a usar nunca, no gastes tiempo normalizándola.

## Resumen: Preparar el Terreno
La limpieza es el 80% del valor inicial. Un dato limpio es un dato que el analista de negocio puede entender sin necesidad de leer el manual técnico de la fuente de origen.
