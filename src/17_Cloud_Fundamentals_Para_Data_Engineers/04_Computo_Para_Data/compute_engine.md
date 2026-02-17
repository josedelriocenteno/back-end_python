# Compute Engine (GCE): Máquinas Virtuales (IaaS)

Compute Engine es el servicio de Google que permite lanzar máquinas virtuales (VMs) en sus centros de datos. En ingeniería de datos, se usa cuando necesitamos control total o potencia bruta para procesos que no caben en modelos serverless.

## 1. Tipos de Máquinas
- **Propósito General (E2, N2):** Equilibrio precio/rendimiento. Para servidores de Airflow o scripts pequeños.
- **Optimizadas para Cómputo (C2):** Para procesos pesados de CPU (ej: codificación de video, simulaciones).
- **Optimizadas para Memoria (M2):** Bases de datos en memoria (Redis, SAP HANA) o procesamiento de datasets gigantes con Pandas/Polars.
- **GPUs:** Puedes añadir tarjetas NVIDIA para modelos de Deep Learning.

## 2. Preemptible VMs (Spot VMs): El ahorro Senior
Son máquinas que Google puede "quitarte" en cualquier momento con un preaviso de 30 segundos si necesita esa potencia para otro cliente.
- **Ventaja:** Cuestan hasta un **80% menos** que una máquina normal.
- **Uso en Data:** Ideales para clústeres de Spark o procesos Batch que pueden fallar y reintentarse sin problemas.

## 3. Discos Persistentes (Persistent Disks)
Igual que el disco duro de tu ordenador.
- **Standard:** Barato, para almacenamiento de backups.
- **SSD:** Rápido, necesario para bases de datos.
- **Local SSD:** El más rápido (conectado físicamente a la VM), pero los datos se borran si apagas la máquina. Solo para almacenamiento temporal (Swap/Scratches).

## 4. Imágenes y Snapshots
- **Imagen:** Un "molde" de una máquina con Linux y Python ya instalados.
- **Snapshot:** Una foto del estado del disco en un momento dado. Vital para recuperarse ante errores humanos.

## 5. Cuándo usar GCE en Data
- Para instalar herramientas que no están en GCP (ej: ClickHouse, MinIO).
- Para clústeres de procesamiento legacy.
- **OJO:** Como Data Engineer, intenta evitar GCE. Es preferible usar servicios gestionados (PaaS) para no gastar tiempo actualizando Linux.

## Resumen: Control Total
Compute Engine te da las llaves del servidor. Es flexible y potente, pero requiere mayor mantenimiento. Úsalo solo cuando las opciones serverless (Cloud Run, Functions) se queden cortas.
