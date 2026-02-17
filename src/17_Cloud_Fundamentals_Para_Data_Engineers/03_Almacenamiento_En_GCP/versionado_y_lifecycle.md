# Versionado y Lifecycle: Control Automático

Mantener todos los archivos para siempre es caro e ineficiente. Cloud Storage ofrece herramientas para automatizar la limpieza y el control de cambios.

## 1. Object Versioning (Versionado)
Si lo activas, cuando subas una nueva versión de `precios.csv`, Google no borrará la antigua; la guardará como una "versión no actual".
- **Utilidad:** Protección contra borrados accidentales o errores en pipelines que sobreescriben datos buenos con basura.
- **Coste:** Cuidado, estás pagando por todas las versiones guardadas.

## 2. Object Lifecycle Management (Ciclo de Vida)
Es un conjunto de reglas que Google ejecuta automáticamente.
- **Regla de ejemplo:** "Si un objeto tiene más de 365 días, cámbialo a la clase `Archive`".
- **Regla de ejemplo:** "Si un objeto está en la carpeta `/tmp/` y tiene más de 7 días, bórralo permanentemente".

## 3. Condiciones del Ciclo de Vida
Puedes crear reglas basadas en:
- Edad del archivo.
- Fecha de creación.
- Si es la versión actual o una antigua.
- Si el objeto ha sido borrado (soft delete).

## 4. Retención de Objetos (Bucket Lock)
Para cumplimiento legal extremo. Puedes configurar un bucket para que **NADIE** (ni siquiera el Owner) pueda borrar un archivo durante X años.
- **Peligro:** Si subes 10TB por error y activas el Bucket Lock, pagarás por esos 10TB durante el tiempo configurado sin poder borrarlos.

## 5. El rol del Ingeniero de Datos
Configura políticas de ciclo de vida en todos tus buckets de logs y staging. No dejes que los archivos temporales se acumulen durante años.

## Resumen: Automatiza el Orden
El versionado te da seguridad frente a errores humanos, y el ciclo de vida te da eficiencia financiera. Ambas herramientas permiten que el Data Lake se gestione solo, reduciendo la carga operativa del equipo.
