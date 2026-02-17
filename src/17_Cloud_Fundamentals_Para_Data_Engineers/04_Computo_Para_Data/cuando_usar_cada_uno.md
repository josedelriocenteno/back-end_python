# ¿Qué cómputo elegir? Tabla de decisión

Como Data Engineer, elegir la herramienta adecuada te ahorrará dinero y trabajo de mantenimiento. Aquí tienes una guía rápida:

## 1. El Árbol de Decisión
1. ¿Es una tarea muy corta (< 10 min) disparada por un evento (subida de archivo)? 
   - **SÍ -> Cloud Functions**.
2. ¿Es un proceso que puede ir en un contenedor Docker y tarda menos de 1 hora?
   - **SÍ -> Cloud Run**.
3. ¿Es una aplicación que requiere un SO específico, GPUs o dura días encendida?
   - **SÍ -> Compute Engine**.
4. ¿Es procesamiento masivo de Terabytes (Big Data) con Spark?
   - **SÍ -> Dataproc** (Veremos esto en el tema 08).
5. ¿Es un pipeline de datos complejo con transformaciones pesadas?
   - **SÍ -> Dataflow** (Veremos esto en el tema 08).

## 2. Comparativa de Gestión
| Característica | Cloud Functions | Cloud Run | Compute Engine |
| :--- | :--- | :--- | :--- |
| **Abstracción** | Código (FaaS) | Contenedor (PaaS) | Servidor (IaaS) |
| **Mantenimiento** | Cero | Mínimo | Alto |
| **Escalabilidad** | Automática | Automática | Manual / Managed Groups |
| **Coste por inactividad** | Gratis | Gratis | Pagas por la VM encendida |

## 3. Enfoque "Serverless First"
La mejor práctica actual es intentar resolver todo con **Cloud Run o Cloud Functions** primero. Solo si encuentras una limitación técnica insalvable (ej: necesitas 200GB de RAM o acceso a hardware especial), pasa a Compute Engine.

## 4. Portabilidad
El código de Cloud Functions está muy "atado" a Google. El código de Cloud Run (Docker) es **portable**: puedes llevarlo a AWS, Azure o a tu propio servidor local sin cambiar casi nada.

## Resumen: Eficiencia Operativa
Elegir bien significa trabajar menos en "fontanería" cloud y más en transformar datos. Prioriza siempre el modelo Serverless para reducir el coste total de propiedad (TCO) de tus pipelines.
