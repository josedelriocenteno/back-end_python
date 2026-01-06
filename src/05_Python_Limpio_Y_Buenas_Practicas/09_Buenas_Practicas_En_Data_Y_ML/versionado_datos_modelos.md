# versionado_datos_modelos.md
=============================

## Versionado de Datos y Modelos en IA/Data

Objetivos:
- Garantizar reproducibilidad de experimentos
- Facilitar colaboración en equipos
- Evitar errores de producción por cambios de datos o modelos
- Mantener trazabilidad de cambios

---

## 1️⃣ POR QUÉ ES IMPORTANTE

- En proyectos de IA, los datos cambian constantemente.
- Modelos entrenados dependen de versiones exactas de los datos.
- Sin versionado:
  - Resultados no reproducibles.
  - Dificultad para depurar errores.
  - Riesgo de desplegar modelos incorrectos en producción.

---

## 2️⃣ VERSIONADO DE DATOS

### Estrategias:

1. **Almacenamiento con hash o checksum**
   - Cada dataset recibe un identificador único basado en su contenido.
   - Ejemplo: SHA256 del CSV o parquet.
   - Permite validar que el dataset usado es exactamente el mismo que en entrenamiento.

2. **Nombres con versión**
   - dataset_v1.csv, dataset_v2.csv
   - Facilita rastreo y rollback si es necesario.

3. **Git para datos pequeños**
   - Para datasets < 100MB, Git funciona bien.
   - Commits claros: `git add dataset_v1.csv -m "Primer dataset limpio"`

4. **Herramientas de versionado para datos grandes**
   - DVC (Data Version Control)
   - Pachyderm
   - MLflow Data
   - Permiten versionar datasets sin saturar Git y con trazabilidad.

---

## 3️⃣ VERSIONADO DE MODELOS

### Estrategias:

1. **Nombres de modelo con versión y metadatos**
   - `modelo_v1_20260106.pkl`
   - Metadata: fecha, datos usados, hiperparámetros.

2. **Almacenamiento centralizado**
   - Carpeta o bucket de modelos con control de versiones.
   - Ejemplo: S3, GCS, MinIO.

3. **Registro de modelos**
   - MLflow, Weights & Biases, Neptune.ai
   - Permite registrar experimentos, métricas y artefactos asociados.
   - Facilita reproducibilidad y despliegue seguro.

4. **Separación de experimentos y producción**
   - Nunca sobrescribir modelos de producción.
   - Versionar modelos experimentales por separado.

---

## 4️⃣ BUENAS PRÁCTICAS REALES

- Mantener un **changelog** de datasets y modelos.
- Incluir **metadatos completos**: fecha, versión, origen de datos, preprocesamiento.
- Usar **checksums o hashes** para asegurar integridad.
- Evitar sobrescribir datasets o modelos antiguos.
- Integrar versionado con **CI/CD** para despliegue reproducible.
- Documentar **cómo generar cada dataset/modelo** desde raw data.

---

## 5️⃣ EJEMPLO DE FLUJO PROFESIONAL

raw_data/ # Datos crudos sin tocar
├── ventas_20260106.csv
└── clientes_20260106.csv

processed_data/ # Datos procesados, versionados
├── ventas_v1.parquet
└── clientes_v1.parquet

models/ # Modelos versionados
├── modelo_regresion_v1.pkl
└── modelo_regresion_v2.pkl

experiments/ # Experimentos con logs
├── exp_001/
│ ├── params.json
│ ├── metrics.json
│ └── modelo.pkl
└── exp_002/


---

## 6️⃣ CONCLUSIÓN

- Versionar **datos y modelos** = reproducibilidad + seguridad.
- Nunca sobrescribir artefactos críticos.
- Usar herramientas profesionales (DVC, MLflow) para proyectos reales.
- Documentar cada cambio y mantener trazabilidad completa.