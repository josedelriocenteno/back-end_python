# Bases de Kubernetes: El siguiente paso

Si Docker es el "Apartamento", **Kubernetes (K8s)** es el administrador de toda la ciudad de apartamentos. Es un orquestador para cuando tienes cientos de contenedores.

## 1. El concepto de Pod
En Kubernetes no lanzamos contenedores directamente. Lanzamos **Pods**.
- Un Pod es el objeto más pequeño y puede contener uno o más contenedores que comparten la misma red e IP.

## 2. Escalado Automático (HPA)
K8s puede mirar el uso de CPU de tu API. Si sube del 70%, lanza automáticamente 5 réplicas nuevas para absorber el tráfico, y las apaga cuando ya no son necesarias.

## 3. Autorreparación (Self-healing)
Si un contenedor muere, K8s lo detecta y lo levanta de nuevo en otro servidor físico si es necesario, basándose en los Healthchecks que definimos antes.

## 4. Actualizaciones sin Caída (Rolling Updates)
K8s puede actualizar tu App de la v1 a la v2 de forma progresiva: lanza un contenedor v2, espera a que esté sano, y solo entonces apaga un v1. El usuario nunca nota el cambio.

## 5. Configuración Declarativa
En lugar de tirar comandos, le pasas archivos YAML a Kubernetes describiendo cómo quieres que sea el mundo.
- `kubectl apply -f deployment.yaml`

## Resumen: De Docker Compose a K8s
Docker Compose es excelente para **un solo servidor**. Kubernetes es para **clústeres de servidores**. Si tu App crece y necesita alta disponibilidad real, Kubernetes será tu hogar final. Por ahora, si tus Dockerfiles son buenos y tus configuraciones son via variables de entorno, estás al 90% listo para K8s.
