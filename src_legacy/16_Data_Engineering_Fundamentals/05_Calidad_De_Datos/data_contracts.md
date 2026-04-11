# Data Contracts: El acuerdo entre Backend y Data

Un **Data Contract** es un acuerdo formal entre los generadores de datos (Backend) y los consumidores de datos (Data Engineering) sobre la estructura y calidad del dato.

## 1. El problema que resuelve
El equipo de Backend cambia un campo en la base de datos de la App para mejorar un proceso. No avisan a Data. El pipeline de Data se rompe. El CEO ve un dashboard vacío por la mañana.

## 2. Qué incluye un Contrato
- **Schema:** Nombres de columnas y tipos de datos exactos.
- **SLA (Service Level Agreement):** "¿Con qué frecuencia se envían los datos?" "¿Qué latencia máxima se permite?".
- **Semántica:** ¿Qué significa exactamente el campo `status`?
- **Propiedad:** ¿Quién es el responsable en Backend si este dato falla?

## 3. Implementación con YAML/JSON Schema
El contrato se define en un archivo que ambos equipos pueden leer y que las herramientas de CI/CD pueden validar automáticamente.
```yaml
dataset: orders
version: 1.0
columns:
  order_id:
    type: integer
    description: "ID único de la transacción"
    constraints: [required, unique]
```

## 4. Beneficios: Desacoplamiento
Con un contrato, el equipo de Backend sabe que si rompen el esquema, el build de su propia App fallará en el test de CI. Esto previene errores en lugar de tener que arreglarlos cuando ya han llegado al pipeline.

## 5. Shift Left (Mover a la izquierda)
Es la filosofía de mover la responsabilidad de la calidad del dato lo más cerca posible de la fuente. No permitas que la basura entre en el pipeline para luego "limpiarla". Haz que el que genera el dato sea responsable de entregarlo limpio.

## Resumen: Comunicación Industrial
Los Data Contracts son para el equipo de datos lo que los Contratos de API (Swagger/OpenAPI) son para el Backend. Son la herramienta definitiva para escalar equipos grandes sin que se rompan las tuberías de información.
