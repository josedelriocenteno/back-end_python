# Docker Networks: Los tres drivers principales

Docker nos permite aislar la red de cada contenedor. Entender los "Drivers" de red es fundamental para diseñar arquitecturas seguras.

## 1. Bridge Network (Por defecto)
Crea una red virtual privada interna. Los contenedores en la misma red `bridge` pueden hablar entre ellos.
- **Uso:** El 90% de los casos. Ideal para comunicar tu App con tu Base de Datos.
- **Detección:** `docker network ls` muestra la red `bridge` por defecto.

## 2. Host Network
El contenedor comparte directamente la red de tu ordenador físico. No hay aislamiento de red.
- **Uso:** Casos de rendimiento extremo donde la red virtual de Docker añade demasiado lag (raro en App web normales).
- **Contra:** Si el contenedor usa el puerto 80, tu PC usa el puerto 80. No puedes correr dos contenedores iguales así.

## 3. None Network
Aislamiento total. El contenedor no tiene tarjeta de red.
- **Uso:** Contenedores de cálculo puro que no necesitan internet ni hablar con otros (ej: procesar un archivo local y cerrarse). Máxima seguridad.

## 4. Overlay Network (Avanzado)
Permite conectar contenedores que están en servidores físicos diferentes (Docker Swarm o Kubernetes).
- **Uso:** Sistemas distribuidos y clústeres.

## 5. Custom Bridge (Recomendado)
No uses el `bridge` por defecto de Docker. Crea tus propias redes:
```bash
docker network create mi_red_backend
```
**¿Por qué?** Porque en redes personalizadas, Docker habilita el **DNS Interno**: los contenedores se pueden llamar por su nombre (ej: `http://db:5432`) en lugar de usar IPs que cambian.

## Resumen: Segmentación
Un desarrollador senior no mete todo en la misma red. Crea redes separadas por proyectos o por capas (ej: red de base de datos vs red pública de la API) para mejorar la seguridad.
