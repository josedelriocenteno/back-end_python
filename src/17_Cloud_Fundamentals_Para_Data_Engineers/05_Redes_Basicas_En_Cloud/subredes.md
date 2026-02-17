# Subredes: Segmentando tu Red

Las **Subredes** (Subnets) son divisiones lógicas dentro de tu VPC. Mientras que la VPC es global, las subredes de Google Cloud son **Regionales**.

## 1. Estructura Regional
Si tienes una VPC llamada `empresa-red`, puedes tener:
- Una subred en `europe-west1` (Bélgica).
- Una subred en `us-central1` (Iowa).
Los recursos (como VMs) deben vivir en una subred específica.

## 2. Direccionamiento IP (CIDR)
Cada subred tiene un rango de direcciones IP privadas (ej: `10.0.1.0/24`). 
- **Tip Senior:** Planifica tus rangos de IP para que no se solapen con otras redes de tu empresa o con tu red de oficina local. Esto facilitará futuras conexiones vía VPN.

## 3. Segmentación por Entorno o Seguridad
Es común crear subredes para diferentes propósitos:
- `subnet-publica`: Para servidores web que deben ser accesibles desde fuera.
- `subnet-privada`: Para bases de datos y procesos de Big Data que no deben tocar internet.

## 4. IP Aliasing
Permite asignar varias direcciones IP a una misma interfaz de red virtual. Muy usado en Kubernetes (GKE) para que cada "Pod" tenga su propia IP dentro de la subred del nodo.

## 5. Expansión de Subredes
Si te quedas sin IPs en una subred, Google permite expandir el rango CIDR sin necesidad de borrar los recursos que ya están dentro. Es una operación transparente y sin tiempo de inactividad.

## Resumen: Organización del Tráfico
Las subredes permiten agrupar recursos por región y por nivel de seguridad. Una buena segmentación facilita la aplicación de reglas de firewall y mejora el rendimiento de la red al reducir el dominio de difusión.
