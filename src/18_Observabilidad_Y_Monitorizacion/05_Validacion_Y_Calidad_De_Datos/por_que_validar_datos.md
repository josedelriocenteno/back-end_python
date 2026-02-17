# ¿Por qué validar los datos?

"Garbage In, Garbage Out" (Si entra basura, sale basura). Este es el mantra del Data Engineer. De nada sirve tener el pipeline más rápido del mundo si los datos que entrega son incorrectos.

## 1. El coste de los datos erróneos
Un error en los datos puede:
*   Hacer que la empresa pierda dinero (ej: precios mal calculados).
*   Provocar decisiones estratégicas equivocadas.
*   Romper los modelos de Machine Learning (que son muy sensibles a valores extremos o nulos).
*   Dañar la reputación del equipo de datos.

## 2. La validación como parte de la Observabilidad
La observabilidad no es solo saber si el servidor está vivo, es saber si el **contenido** del mensaje es correcto.
*   **Monitorización:** "El archivo llegó".
*   **Validación:** "El archivo llegó, tiene 1000 filas y ninguna columna de precio es negativa".

## 3. Prevención vs. Detección
*   **Prevención:** El pipeline se para si el dato es malo (**Data Contract**). Evitas que la basura llegue al Data Warehouse.
*   **Detección:** El pipeline termina, pero recibes una alerta avisando de que la calidad es baja.

## 4. Confianza del Consumidor
Si los analistas y científicos de datos saben que hay un sistema de validación robusto, confiarán en tus tablas. Si no, dedicarán el 50% de su tiempo a "limpiar" y "comprobar" los datos manualmente, lo cual es ineficiente.

## 5. El "Data Downtime"
Igual que el sistema puede estar "caído" por un fallo de red, el sistema está "caído" si el dato no es fiable. La validación reduce el **Data Downtime** detectando los errores en la fuente antes de que se propaguen.

## Resumen: Calidad por diseño
Validar datos no es una opción, es una obligación. Es la diferencia entre ser un "pasatareas" y ser un Ingeniero de Datos profesional que garantiza el activo más valioso de la empresa: la información.
