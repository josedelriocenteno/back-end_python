# Regiones y Zonas: Alta Disponibilidad y Latencia

Google Cloud no es un único lugar físico. Es una red global de centros de datos repartidos por todo el mundo. Entender cómo se organizan es clave para que tus pipelines sean rápidos y resistentes a fallos.

## 1. Región: El área geográfica
Una **Región** es una ubicación geográfica específica (ej: `europe-west1` en Bélgica, `us-central1` en Iowa).
- **Latencia:** Siempre intenta colocar tus datos y tus servicios de cómputo en la región más cercana a tus usuarios o a tu oficina.
- **Cumplimiento:** Países con leyes estrictas (como España) pueden exigir que los datos no salgan de la región europea.

## 2. Zona: El centro de datos
Dentro de cada Región hay varias **Zonas** (ej: `europe-west1-b`, `europe-west1-c`). Cada zona representa uno o más centros de datos físicos independientes.
- **Aislamiento:** Las zonas están conectadas por redes de alta velocidad pero separadas físicamente. Si un incendio destruye una zona, las otras seguirán funcionando.

## 3. Alta Disponibilidad (High Availability - HA)
Para un Data Engineer, esto significa configurar los servicios para que vivan en varias zonas a la vez.
- **Multi-zonal:** Si tu base de datos está en 2 zonas, si una cae, la otra toma el mando automáticamente.
- **Multi-regional:** Tus datos se replican en diferentes regiones (ej: Europa y EEUU). Máxima seguridad ante desastres naturales masivos.

## 4. Recursos Globales vs. Regionales vs. Zonales
- **Globales:** Cloud DNS, IAM. Funcionan igual en todo el mundo.
- **Regionales:** BigQuery (se puede configurar regional), Cloud Storage (cubos regionales).
- **Zonales:** Máquinas virtuales (Compute Engine). Viven en una zona específica.

## 5. El coste de la geografía
- Elegir diferentes regiones puede cambiar el precio de los servicios.
- **Cuidado:** Mover datos entre regiones (Egress) suele tener un coste por Gigabyte. Mover datos entre zonas de la misma región suele ser gratis o mucho más barato.

## Resumen: Ubicación Inteligente
Diseña tus sistemas pensando en dónde están tus datos. Minimiza la latencia para los usuarios y maximiza la redundancia para evitar pérdidas de información en caso de fallo técnico en un centro de datos.
