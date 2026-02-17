# Datos Semi-estructurados: Flexibilidad y Esquema en el Vuelo

Los datos semi-estructurados no encajan en una tabla rígida pero contienen etiquetas o marcadores que separan los elementos. Son el estándar en la comunicación entre sistemas modernos.

## 1. Formatos Clave
- **JSON:** El rey de las APIs de Backend.
- **XML:** El abuelo de los datos semi-estructurados, todavía común en sistemas financieros y gubernamentales.
- **Avro:** Formato binario eficiente que guarda el esquema junto con el dato.

## 2. Esquema en el Vuelo (Schema-on-Read)
A diferencia de SQL (Schema-on-Write), donde el dato debe cumplir el esquema para entrar, en los datos semi-estructurados el esquema se interpreta **cuando se lee el dato**.
- Esto permite que cada registro tenga campos diferentes.

## 3. Uso en Ingeniería de Datos
Se usan principalmente en la **fase de ingesta**. La mayoría de las APIs devuelven un JSON que el ingeniero de datos debe "aplanar" para convertirlo en una tabla estructurada útil.

## 4. Ventajas: Evolución del Esquema
Si una API añade un campo nuevo, tu pipeline no se rompe. Simplemente el nuevo campo se ignora o se guarda hasta que decidas usarlo. Esto es vital en entornos que cambian rápido.

## 5. El peligro de la inconsistencia
La flexibilidad tiene un precio: puedes acabar con datos basura o tipos inconsistentes (ej: un registro tiene la edad como `25` y otro como `"vinticinco"`). El ingeniero de datos debe añadir validaciones extra.

## Resumen: El puente entre mundos
Los datos semi-estructurados nos dan la agilidad necesaria para capturar información sin las restricciones de una base de datos tradicional, permitiendo que la arquitectura sea mucho más dinámica.
