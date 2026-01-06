# debugging_en_produccion.md
============================

Objetivo:
---------
Aprender **cómo depurar en entornos de producción** de manera profesional, minimizando riesgos y manteniendo trazabilidad.

---

## 1️⃣ PRINCIPIOS GENERALES

1. **Evitar prints y breakpoints interactivos**:  
   - Interrumpen la ejecución y afectan usuarios reales.
   - Pueden exponer datos sensibles.

2. **Usar logs estructurados**:  
   - Logs persistentes con niveles (INFO, WARNING, ERROR, CRITICAL).  
   - Incluir contexto: módulo, función, ID de usuario/registro, timestamps.

3. **Reproducibilidad primero**:  
   - Intentar recrear el error en un entorno de staging o desarrollo antes de tocar producción.

4. **Fail-safe y monitorización**:  
   - Asegurarse de que cualquier debugging remoto o logging avanzado no rompa el flujo de la aplicación.

---

## 2️⃣ HERRAMIENTAS RECOMENDADAS

| Herramienta        | Uso principal                                     |
|-------------------|--------------------------------------------------|
| Logging + exc_info | Captura tracebacks completos                     |
| Sentry / Rollbar   | Monitoreo de errores, alertas y contextos       |
| Remote Debuggers  | pdb remoto o `remote-pdb` para inspección segura|
| Snapshots de DB   | Inspección de datos problemáticos sin afectar usuarios|

---

## 3️⃣ QUÉ HACER

1. **Registrar el error con contexto completo**
   ```python
   import logging

   try:
       procesar_valores(x, y)
   except Exception:
       logging.error("Error procesando valores", exc_info=True)

    Capturar datos relevantes sin exponer sensibles

        IDs internos, estados de objetos, tamaños de listas

        Evitar registrar contraseñas, tokens, PII.

    Crear entornos de staging para reproducir errores

        Duplica la situación real sin afectar usuarios finales.

        Permite debugging seguro y pruebas de corrección.

    Monitorear métricas y alertas

        Trackear tasas de error por endpoint, módulo o función.

        Configurar alertas para errores críticos.

    Documentar hallazgos

        Registrar causas, solución propuesta y cambios realizados.

        Facilita debugging futuro y trabajo en equipo.

4️⃣ QUÉ NO HACER

    ❌ Ejecutar print o breakpoint interactivo en producción.

    ❌ Cambiar código directamente sin pruebas.

    ❌ Registrar datos sensibles o masivos.

    ❌ Ignorar errores y confiar en “a ver qué pasa”.

    ❌ Depurar solo con intuición; siempre basarse en logs y trazas verificables.

5️⃣ EJEMPLOS PROFESIONALES
Correcto:

import logging

def procesar_usuario(user_id):
    try:
        user = obtener_usuario(user_id)
        procesar_datos(user)
    except Exception as e:
        logging.error(f"Error procesando usuario {user_id}", exc_info=True)
        raise  # Re-lanzar si es crítico para fail-fast

Incorrecto:

def procesar_usuario(user_id):
    try:
        user = obtener_usuario(user_id)
        procesar_datos(user)
    except:
        print("Error")  # ❌ No da contexto ni persistencia

6️⃣ BUENAS PRÁCTICAS

    Siempre fallar rápido y registrar información completa.

    Nunca afectar usuarios con debugging interactivo.

    Usar herramientas de monitorización y alertas para detectar patrones.

    Mantener logs estructurados que puedan analizarse automáticamente.

    Mantener un workflow de staging → producción para pruebas antes de desplegar correcciones.

✅ Resumen

    Debugging en producción requiere precaución, control y trazabilidad.

    Logs estructurados y herramientas como Sentry permiten inspección segura.

    Evitar prints, breakpoints y datos sensibles.

    Siempre reproducir en entornos controlados antes de cambiar código en producción.