# Validaciones Básicas: El Checklist Inicial

Antes de usar herramientas complejas, debes asegurarte de que tus datos cumplen estas reglas básicas. Es lo que llamamos "Sanity Checks" (Chequeos de cordura).

## 1. Validaciones de Estructura (Esquema)
*   **Columnas:** ¿Están todas las columnas esperadas? ¿Han aparecido columnas nuevas?
*   **Tipos de Datos:** ¿La fecha es realmente una fecha o es un string? ¿El precio es un número?
*   **Formato:** ¿Los correos electrónicos tienen una `@`? ¿Los códigos postales siguen el formato correcto?

## 2. Validaciones de Contenido
*   **Nulos (Nullability):** ¿Hay campos obligatorios que vienen vacíos?
*   **Unicidad (Uniqueness):** ¿Hay IDs de usuario duplicados donde no debería haberlos?
*   **Rangos (Range):** ¿Hay edades negativas o precios de 1 millón de euros en una tienda de ropa?

## 3. Validaciones de Volumen
*   **Recuento de filas:** Si ayer procesamos 10.000 filas y hoy solo 10, algo va mal.
*   **Tamaño del archivo:** Si el archivo pesa 0 bytes, el proceso de extracción ha fallado.

## 4. Validaciones de Relación (Referencial)
*   **Integridad:** ¿Este `id_producto` existe en mi tabla maestra de productos? 
*   **Carencia:** ¿Hay ventas que no tienen un cliente asociado?

## 5. Validaciones de Negocio (Lógica)
*   **Consistencia:** ¿La suma de las líneas de la factura coincide con el total de la factura?
*   **Orden temporal:** ¿La fecha de entrega es posterior a la fecha de compra?

## Resumen: Los cimientos de la calidad
Estas validaciones son sencillas de implementar pero detectan el 90% de los problemas habituales. Automatizar estos chequeos al final de cada fase del pipeline te ahorrará horas de debugging y explicaciones incómodas.
