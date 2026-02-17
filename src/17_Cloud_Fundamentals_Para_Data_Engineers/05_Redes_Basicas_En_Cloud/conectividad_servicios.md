# Conectividad de Servicios: Rompiendo Silos

Los servicios de datos de Google (como BigQuery o Cloud Storage) no viven "dentro" de tu VPC, sino en la red pública de Google. ¿Cómo hablamos con ellos de forma segura?

## 1. Private Google Access (Acceso Privado a APIs)
Permite que una máquina virtual con solo IP privada pueda hablar con BigQuery, Cloud Storage o Cloud Pub/Sub sin pasar por internet.
- Es una simple "casilla de verificación" en la configuración de la subred.
- **Resultado:** Tráfico más rápido, más seguro y sin coste de "Egress" a internet.

## 2. VPC Peering (Emparejamiento)
Une dos VPCs (ej: la de tu equipo y la del equipo de otro departamento) para que se vean como si fueran una sola red privada.
- Es bidireccional.
- El tráfico no sale de la red de Google, por lo que es ultra-rápido.

## 3. Private Service Connect (PSC)
Es la forma moderna de consumir servicios de terceros o de Google como si fueran una IP privada dentro de tu red. Muy útil para conectar a bases de datos de socios o servicios externos de forma segura.

## 4. Cloud VPN
Conecta tu red local (oficina) con tu VPC de Google Cloud a través de un túnel cifrado por internet. Imprescindible para que tus analistas puedan conectar desde sus ordenadores a la base de datos de GCP de forma privada.

## 5. Cloud Interconnect
Si una VPN no es suficiente por volumen de datos, puedes tirar un cable de fibra física directo desde tu oficina al data center de Google. Ofrece la máxima velocidad y fiabilidad posible.

## Resumen: Comunicación Fluida
La red debe facilitar el trabajo, no ser un obstáculo. Private Google Access es obligatorio en cualquier arquitectura de datos seria. VPC Peering y VPNs permiten que la información fluya entre equipos y oficinas manteniendo la seguridad de una red privada.
