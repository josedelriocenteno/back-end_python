# Proyectos y Facturación: Organización Real

En Google Cloud, todo lo que crees debe pertenecer a un **Proyecto**. No puedes crear nada "en el aire". El proyecto es el contenedor básico de recursos, permisos y, sobre todo, costes.

## 1. El Proyecto: La unidad de aislamiento
Cada proyecto tiene:
- **Nombre:** Un nombre amigable (ej: "Proyecto Producción").
- **Project ID:** Un identificador único global (ej: `mi-empresa-prod-123`). Nunca cambia.
- **Project Number:** Un número generado por Google.

## 2. Jerarquía de Recursos
Google organiza las empresas como un árbol:
1. **Organización:** (ej: `miempresa.com`). El nodo raíz.
2. **Carpetas:** (ej: `Departamento Data`, `Departamento Marketing`). Para agrupar proyectos.
3. **Proyectos:** Donde viven las máquinas y bases de datos.
4. **Recursos individuales:** Cuentas de servicio, buckets, tablas.

## 3. Billing Account (Cuenta de Facturación)
Es el "método de pago". Una Billing Account puede estar conectada a muchos proyectos.
- **Tip Senior:** Nunca mezcles proyectos de Desarrollo con Producción en la misma Billing Account si quieres tener un control de costes granular.

## 4. Cuotas (Quotas)
Google impone límites a los proyectos para evitar facturas accidentales astronómicas o abusos.
- **Tipos:** Límites de tasa (X peticiones por segundo) y límites de recursos (X CPUs en total).
- Si necesitas más potencia, debes solicitar un aumento de cuota en el panel de control.

## 5. Etiquetas (Labels)
Son pares `clave:valor` que añades a los recursos (ej: `entorno:prod`, `equipo:data`, `coste:alto`).
- Son vitales para el equipo financiero. Al final del mes, puedes ver exactamente cuánto se ha gastado el equipo de Data en el entorno de Producción filtrando por estas etiquetas.

## Resumen: Orden es Dinero
Una mala organización de proyectos y falta de etiquetas lleva al caos financiero y de seguridad. Diseña tu jerarquía de carpetas y proyectos de forma lógica antes de empezar a crear infraestructura masiva.
