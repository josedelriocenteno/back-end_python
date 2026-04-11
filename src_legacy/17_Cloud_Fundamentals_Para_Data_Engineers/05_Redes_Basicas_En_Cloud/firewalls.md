# Firewalls: Los guardianes de la puerta

Un Firewall de VPC es un conjunto de reglas que controlan qué tráfico entra y sale de tus máquinas virtuales y servicios. Son "stateful", lo que significa que si permites la entrada, la respuesta sale automáticamente.

## 1. Reglas por Defecto
Google aplica 4 reglas básicas para protegerte al crear una red:
- Bloquear toda la entrada (excepto ping y algunos servicios básicos).
- Permitir toda la salida hacia internet.

## 2. Anatomía de una Regla
Para crear una regla necesitas definir:
- **Dirección:** Entrada (Ingress) o Salida (Egress).
- **Acción:** Permitir o Denegar.
- **Protocolo y Puertos:** TCP (80, 443, 5432 para Postgres), UDP o ICMP.
- **Origen/Destino:** Un rango de IPs o, mucho mejor, un **Target Tag**.

## 3. Target Tags: Seguridad Basada en Nombres
No uses direcciones IP fijas en tus firewalls. Usa etiquetas.
- **Ejemplo:** Crea un tag llamado `base-datos`.
- **Regla:** "Permitir puerto 5432 desde cualquier máquina que tenga el tag `backend-app` hacia las máquinas que tengan el tag `base-datos`".
- Da igual cuántas máquinas creas o borres; si tienen la etiqueta correcta, la seguridad se aplica sola.

## 4. Prioridades
Las reglas de firewall tienen una prioridad (0 a 65535). Las reglas con números más bajos se ejecutan primero. 
- **Uso:** Puedes tener una regla general que bloquee todo (prioridad 1000) y una regla específica para tu IP de oficina (prioridad 500) que sí permita el paso.

## 5. Firewall Logs
Puedes habilitar el registro de logs del firewall. Verás cada intento de conexión fallido. Vital para detectar ataques de fuerza bruta o entender por qué tu script de Python no puede conectar a la base de datos.

## Resumen: Bloqueo por Defecto
Dudar siempre es la mejor práctica. Solo abre los puertos que necesites estrictamente y usa Target Tags para mantener la flexibilidad. Un firewall bien configurado es la barrera que evita que tus datos privados acaben en manos equivocadas.
