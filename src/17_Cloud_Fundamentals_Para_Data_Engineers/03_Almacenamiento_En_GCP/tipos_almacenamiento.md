# Storage Classes: Optimizando el Coste

En Cloud Storage, no todos los archivos necesitan estar disponibles en milisegundos todo el tiempo. Google ofrece diferentes "clases" según la frecuencia con la que accedas al dato.

## 1. Standard (Frecuente)
Ideal para datos que usas a diario.
- **Uso:** Pipelines activos, logs de ayer, archivos que se consultan constantemente.
- **Coste:** Almacenamiento más caro, pero acceso gratis (sin coste de recuperación).

## 2. Nearline (Infrecuente - 30 días)
Para datos que esperas usar menos de una vez al mes.
- **Uso:** Copias de seguridad mensuales, reportes de cierre de mes.
- **Compromiso:** Mínimo 30 días de permanencia. Si lo borras antes, pagas una penalización.

## 3. Coldline (Frío - 90 días)
Para datos que esperas usar menos de una vez cada trimestre.
- **Uso:** Datos históricos de años anteriores que rara vez se consultan pero deben guardarse por ley.
- **Compromiso:** Mínimo 90 días de permanencia.

## 4. Archive (Archivo - 365 días)
El almacenamiento más barato de Google (centavos por Terabyte).
- **Uso:** Cumplimiento legal a largo plazo (ej: guardar facturas 5 años). 
- **Coste:** Recuperar el dato es muy caro. Úsalo solo para lo que esperas no tener que leer NUNCA.

## 5. Autoclass: La gestión inteligente
Si no quieres pensar en esto, puedes activar **Autoclass**. Google monitoriza el uso de cada archivo y, si un archivo no se lee en 30 días, lo mueve automáticamente de Standard a Nearline para ahorrarte dinero.

## Resumen: Estrategia de Costes
Un Data Engineer Senior ahorra miles de euros a su empresa simplemente moviendo los datos históricos a clases de almacenamiento más frías. La clave es saber equilibrar el coste de guardar vs. el coste de recuperar.
