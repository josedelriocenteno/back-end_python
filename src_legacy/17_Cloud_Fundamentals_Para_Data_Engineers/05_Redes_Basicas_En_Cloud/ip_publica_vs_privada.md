# IP Pública vs. Privada: Seguridad y NAT

En la nube, la gestión de las direcciones IP determina quién puede ver a quién y desde dónde.

## 1. IP Privada (Internal IP)
Cada recurso en una VPC recibe una IP privada del rango de su subred (ej: `10.0.1.5`).
- Solo es visible dentro de la VPC.
- **Ventaja:** Tráfico gratis (dentro de la misma zona) y seguridad máxima.
- **Uso:** Bases de datos, clústeres de Spark internos, procesos ETL.

## 2. IP Pública (External IP)
Es una dirección visible desde todo internet.
- **Efemera:** Cambia si apagas y enciendes la máquina.
- **Estática (Reservada):** Google te garantiza que nunca cambiará. Útil para servidores web.
- **Peligro:** Tener una IP pública significa que cualquier hacker del mundo puede intentar atacar tu puerto 22 (SSH).

## 3. Cloud NAT: Salida Segura a Internet
¿Y si mi servidor de datos necesita bajar una actualización de Python o conectar a una API externa (como OpenAI) pero no quiero que tenga IP pública por seguridad?
- **Solución:** Cloud NAT. Permite a los recursos con solo IP privada salir a internet para hacer peticiones, pero impide que nadie desde internet inicie una conexión hacia ellos.

## 4. IP Externa Estática vs. Dinámica
Reserva siempre IPs estáticas para servicios críticos. Si tu cliente ha puesto tu IP en su "lista blanca" (whitelist) y tu IP cambia porque reiniciaste el servidor, el sistema dejará de funcionar.

## 5. El coste de la IP Pública
Google cobra por cada hora que una IP pública estática NO se esté usando. Esto es para evitar que la gente "reserve" IPs y las deje abandonadas. Si no la necesitas, llibérala.

## Resumen: Ocultos por Defecto
Como Data Engineer, tu objetivo es que el 99% de tu infraestructura tenga **solo IP privada**. Usa Cloud NAT para hablar con el mundo exterior y mantén tu red interna protegida y lejos de los escaneos públicos de internet.
