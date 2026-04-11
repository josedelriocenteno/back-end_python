# Buenas Prácticas en Cloud: El Checklist del Senior

Trabajar en la nube sin un orden claro es la forma más rápida de arruinar un presupuesto o tener una brecha de seguridad. Sigue estos principios desde el primer día.

## 1. El Principio de Aislamiento
- Usa proyectos diferentes para **Desarrollo (DEV)**, **Pruebas (STG)** y **Producción (PROD)**.
- Nunca permitas que un script de DEV pueda escribir en una tabla de PROD por error.

## 2. Control de Costes Proactivo
- Configura **Alertas de Presupuesto (Budgets)**. Que Google te envíe un email cuando el gasto llegue al 50%, 80% y 100% de lo previsto.
- Revisa semanalmente los recursos que no se usan. Una máquina virtual encendida sin hacer nada es tirar dinero.

## 3. Nomenclatura Estándar
Define cómo se llaman las cosas. Evita nombres como `test_pipeline_2`.
- **Sugerencia:** `[env]-[equipo]-[app]-[tipo]-[id]`.
- **Ejemplo:** `prod-data-ventas-bucket-01`.

## 4. Infraestructura como Código (IaC)
A medida que crezcas, evita crear cosas haciendo clicks en la consola. Usa herramientas como **Terraform**.
- Esto permite guardar tu infraestructura en Git, ver quién cambió qué y clonar un entorno deProducción a Desarrollo en segundos.

## 5. Seguridad: Mínimo Privilegio
No uses tu cuenta de usuario personal para que los scripts se conecten a la base de datos. Usa **Service Accounts** y dales solo los permisos exactos que necesitan.

## 6. Documentación "In-Cloud"
Usa las descripciones de los proyectos y las etiquetas. Si alguien ve un recurso desconocido, debería poder saber para qué sirve solo leyendo sus metadatos.

## Resumen: Construir para el Futuro
Un entorno cloud profesional debe ser limpio, predecible y seguro. Aplicar estas buenas prácticas te ahorrará cientos de horas de depuración y evitará "sustos" en la factura a final de mes.
