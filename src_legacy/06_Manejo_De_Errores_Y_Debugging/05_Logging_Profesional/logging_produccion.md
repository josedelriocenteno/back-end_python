# logging_produccion.md
=======================

Objetivo:
---------
Aprender **qué información registrar en producción** y **qué evitar**, para mantener logs útiles, seguros y eficientes.

---

## 1️⃣ PRINCIPIOS GENERALES

1. **Relevancia:** Solo loguear información que ayude a monitoreo, debugging o auditoría.
2. **Seguridad:** Nunca registrar contraseñas, tokens, datos personales sensibles (PII) o información financiera sin anonimizar.
3. **Niveles adecuados:** Ajustar según gravedad:
   - DEBUG → desarrollo
   - INFO → flujo normal de producción
   - WARNING → eventos inesperados pero no críticos
   - ERROR → fallos en operaciones
   - CRITICAL → fallos graves del sistema
4. **Eficiencia:** Evitar logs excesivos que saturen disco o sistema de monitoreo.

---

## 2️⃣ QUÉ LOGUEAR

### 2.1 Flujo del sistema
- Inicio y finalización de procesos importantes.
- Ejemplo: “Servicio de envío de emails iniciado” / “Servicio finalizado”.

### 2.2 Errores y excepciones
- Todas las excepciones críticas deben registrarse.
- Incluir contexto: módulo, función, ID de usuario o registro afectado.

### 2.3 Métricas importantes
- Cantidad de registros procesados.
- Tiempos de ejecución de procesos críticos.
- Indicadores de rendimiento y disponibilidad.

### 2.4 Eventos inesperados
- Datos incompletos o inválidos, pero que no detienen el sistema.
- Comportamiento anómalo de terceros (APIs, sistemas externos).

---

## 3️⃣ QUÉ NO LOGUEAR

1. **Datos sensibles**
   - Contraseñas, PINs, tokens de acceso, números de tarjeta.
2. **Información redundante o trivial**
   - Cada operación menor o variable temporal.
3. **Mensajes DEBUG en producción**
   - Generan ruido y saturan logs.
4. **Mensajes de print sin formato**
   - No permiten filtrado ni trazabilidad.

---

## 4️⃣ EJEMPLOS PRÁCTICOS

```python
import logging

logger = logging.getLogger("produccion")
logger.setLevel(logging.INFO)

# Correcto
logger.info("Servicio iniciado")
logger.warning("Registro incompleto: ID=123")
logger.error("Error procesando registro: ID=456")

# Incorrecto
usuario_password = "123456"
logger.info(f"Password del usuario: {usuario_password}")  # ❌ NO
