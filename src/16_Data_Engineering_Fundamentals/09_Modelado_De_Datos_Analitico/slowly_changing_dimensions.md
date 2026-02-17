# Slowly Changing Dimensions (SCD): Gestionando el cambio

¿Qué pasa si un cliente que vivía en un barrio humilde se muda a una zona de lujo? ¿Debemos actualizar sus compras antiguas (falseando la historia) o mantener el rastro de dónde vivía cuando hizo la compra? Las **SCD** resuelven este dilema.

## 1. SCD Tipo 0 (Retención)
El valor original nunca cambia.
- **Ejemplo:** Fecha de nacimiento de un cliente. Si intentas cambiarlo, el sistema lo ignora.

## 2. SCD Tipo 1 (Sobreescritura)
Sobreescribimos el valor antiguo con el nuevo.
- **Consecuencia:** Perdemos el historial. Si el cliente cambia de país, todos sus pedidos del año pasado parecerán haber ocurrido en el país nuevo.
- **Uso:** Corregir errores tipográficos (ej: corregir el nombre mal escrito).

## 3. SCD Tipo 2 (Historial de Versiones) - EL ESTÁNDAR
Añadimos una nueva fila para el mismo cliente con el nuevo valor.
- Usamos columnas de control: `valid_from`, `valid_to` e `is_current`.
- **Ventaja:** Podemos saber dónde vivía el cliente en cualquier punto del tiempo. Es la forma más profesional de mantener la integridad histórica.

## 4. SCD Tipo 3 (Campos Anteriores)
Mantenemos el valor actual y el valor anterior en la misma fila.
- `ciudad_actual`, `ciudad_anterior`.
- **Límite:** Solo permite ver el último cambio. Si el cliente se muda por tercera vez, perdemos el primer dato.

## 5. Implementación con dbt Snaphots
Gestionar SCD Tipo 2 a mano con SQL es propenso a errores. Herramientas como dbt tienen una funcionalidad llamada `snapshots` que genera automáticamente las columnas `valid_from` y `valid_to` comparando los datos nuevos con los viejos.

## Resumen: La Memoria del Negocio
Saber gestionar el cambio en las dimensiones es lo que diferencia a un almacén de datos de una simple copia de la base de datos de producción. El historial es el activo más valioso de la analítica.
