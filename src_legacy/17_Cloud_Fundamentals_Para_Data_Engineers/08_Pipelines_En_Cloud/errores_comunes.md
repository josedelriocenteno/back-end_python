# Errores comunes en Pipelines Cloud

Incluso los mejores arquitectos cometen errores al principio. Aprender de estos fallos típicos te ahorrará muchas horas de frustración y dinero a la empresa.

## 1. El "SELECT *" en BigQuery
- **Error:** Lanzar un `SELECT * FROM tabla_enorme` dentro de un pipeline o dashboard.
- **Consecuencia:** Facturas astronómicas al leer columnas que no necesitas.
- **Solución:** Selecciona solo las columnas necesarias y usa particionado por fecha siempre.

## 2. No manejar el "Backfill"
- **Error:** Diseñar un pipeline que solo procesa "los datos de hoy".
- **Consecuencia:** Si el sistema falla 3 días, cuando lo arregles, habrás perdido 3 días de datos si no puedes re-ejecutarlo para fechas pasadas.
- **Solución:** Usa variables de fecha (`ds` en Airflow) para que tus pipelines sean dinámicos.

## 3. Service Accounts con demasiados permisos
- **Error:** Darle el rol de `Owner` o `Editor` a una cuenta de servicio para que un script pueda leer un archivo.
- **Consecuencia:** Si alguien roba esa cuenta, tiene las llaves de toda la empresa.
- **Solución:** Usa roles específicos como `Storage Object Viewer`.

## 4. Confundir Airflow con una base de datos
- **Error:** Hacer procesado pesado de datos (ej: entrenar un modelo de ML o mover 10GB con Pandas) dentro de los workers de Airflow.
- **Consecuencia:** El entorno de Cloud Composer se cae constantemente.
- **Solución:** Airflow lanza el trabajo en otro sitio (BigQuery, Spark, Cloud Run), no lo hace él.

## 5. Olvidar los Límites de Cuota (Quotas)
- **Error:** Lanzar 1000 Cloud Functions a la vez sin mirar los límites de tu proyecto.
- **Consecuencia:** Las funciones fallan aleatoriamente y los datos se pierden.
- **Solución:** Revisa el panel de IAM & Admin -> Quotas antes de escalar masivamente un proceso.

## Resumen: Ingeniería de Prevención
Un Data Engineer Senior gasta el 50% de su tiempo diseñando cómo el sistema debe fallar con elegancia. Evitar estos errores básicos es el primer paso para construir una infraestructura de datos de clase mundial.
