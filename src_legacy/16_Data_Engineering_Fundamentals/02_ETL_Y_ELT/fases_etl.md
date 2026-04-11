# Fases de un Pipeline: Extract, Transform, Load

Desglosamos el proceso atómico de mover datos. Un fallo en cualquiera de estas fases rompe la confianza del negocio en el dato.

## 1. E (Extract - Extracción)
Conectar con las fuentes y traer el dato.
- **Retos:** Autenticación en APIs, gestión de cuotas (Rate Limits), detección de nuevos registros (CDC - Change Data Capture) para no bajar todo de nuevo cada vez.
- **Buenas Prácticas:** Haz la extracción lo más rápida y ligera posible. No transformes nada aquí, solo "copia y pega" al área de tránsito (Staging).

## 2. T (Transform - Transformación)
La "magia" donde el dato cobra sentido.
- **Limpieza:** Quitar duplicados, corregir formatos de fecha, normalizar textos.
- **Aplanado:** Convertir JSONs complejos en tablas planas SQL.
- **Enriquecimiento:** Unir el ID del usuario con su nombre y país consultando otra tabla o API.
- **Cálculo:** Generar métricas (ej: `precio_total = cantidad * precio_unitario`).

## 3. L (Load - Carga)
Depositar el dato en su hogar final.
- **Modos de carga:**
  - **Full Load:** Borrar todo y volver a escribir (solo para tablas pequeñas).
  - **Incremental:** Solo añadir las filas nuevas (rápido y escalable).
  - **Upsert:** Actualizar si existe, insertar si no. Vital para corregir datos pasados.

## 4. El Área de Staging (Aterrizaje)
Nunca cargues directamente en las tablas finales. Usa una zona intermedia (Staging) donde los datos llegan crudos. Si algo falla en la transformación, no habrás corrompido tus tablas maestras.

## 5. Auditoría de Fases
Monitoriza cuánto tiempo tarda cada fase. Si la extracción de repente tarda el doble, es señal de que la fuente de datos ha crecido o que hay un cuello de botella en la red.

## Resumen: Orden y Concierto
Dividir el trabajo en fases claras permite que el pipeline sea modular. Si cambia la fuente de datos, solo tienes que reescribir la fase **E**, manteniendo la lógica de negocio de la fase **T** intacta.
