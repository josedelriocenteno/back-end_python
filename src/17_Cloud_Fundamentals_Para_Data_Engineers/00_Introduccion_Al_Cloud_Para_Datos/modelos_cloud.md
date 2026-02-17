# Modelos Cloud: IaaS, PaaS, SaaS para Datos

No todos los servicios cloud se usan igual. Dependiendo de cuánto control (y cuánto trabajo) quieras tener, elegirás un modelo u otro.

## 1. IaaS (Infrastructure as a Service)
Te dan el "hierro" virtual. Tú te encargas del Sistema Operativo, parches y software.
- **Ejemplo:** Compute Engine (VMs).
- **En Data:** Usarías IaaS si quieres instalar una versión muy específica de Hadoop o Kafka que no existe como servicio gestionado.

## 2. PaaS (Platform as a Service)
Te dan la plataforma lista para ejecutar tu código. Google se encarga del servidor y el SO.
- **Ejemplo:** Cloud Run, Cloud Functions.
- **En Data:** Subes tu script de Python que limpia datos y Google se encarga de escalarlo y ejecutarlo.

## 3. SaaS (Software as a Service)
Te dan el software listo para usar vía web o API.
- **Ejemplo:** Google Analytics, Salesforce.
- **En Data:** BigQuery es casi un SaaS/PaaS híbrido; no configuras nada, solo lanzas queries SQL y pagas por los datos procesados.

## 4. El modelo "Serverless"
Es la evolución del PaaS. Significa que tú no gestionas servidores en absoluto. El sistema se "enciende" cuando llega un dato, lo procesa y se "apaga" solo. 
- Es el modelo ideal para un Data Engineer moderno: Máxima eficiencia y cero mantenimiento de infraestructura.

## 5. Shared Responsibility (Responsabilidad Compartida)
- **Del Cloud:** Google es responsable de que el data center no se queme y el hardware funcione.
- **En el Cloud:** Tú eres responsable de quién tiene acceso a tus datos y de no dejar tu base de datos abierta a todo internet.

## Resumen: Elegir el nivel de abstracción
- ¿Quieres controlar hasta el último bit del kernel de Linux? -> **IaaS**.
- ¿Quieres preocuparte solo de tu código? -> **PaaS/Serverless**.
- ¿Quieres que el sistema funcione y solo meter datos? -> **SaaS**.
