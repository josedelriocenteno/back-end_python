# Errores de Red Comunes (Troubleshooting)

"¡No conecta!" es el grito de guerra cuando empiezas con redes en Docker. Aquí el manual de supervivencia.

## 1. El error de Bind 0.0.0.0
Si tu App backend (Gunicorn/Uvicorn) está configurada para escuchar en `127.0.0.1`, **no funcionará en Docker**.
- **Por qué:** `127.0.0.1` dentro del contenedor es solo el contenedor. Docker Engine, que está "fuera", no podrá enviarle tráfico.
- **Solución:** Configura tu App para escuchar en `0.0.0.0` (todas las interfaces del contenedor).

## 2. Name Resolution failure (EAI_AGAIN)
Si intentas conectar a `db` y te da un error de resolución de nombre.
- **Causa:** Probablemente los contenedores no están en la misma red personalizada o estás usando el `bridge` por defecto que no tiene DNS.
- **Solución:** `docker network connect mi_red contenedor_app`.

## 3. Conflictos de Puertos
`Error starting userland proxy: listen tcp 0.0.0.0:80: bind: address already in use`
- **Causa:** Ya tienes algo corriendo en el puerto 80 de tu ordenador (quizás otro Docker, un Apache viejo o Skype).
- **Solución:** Cambia el puerto del host: `-p 8081:80`.

## 4. El Firewall del Host (iptables)
En Linux, Docker manipula directamente las reglas de `iptables`.
- **Problema:** Si tienes un firewall (como UFW) mal configurado, puede entrar en conflicto con Docker y bloquear el tráfico entrante a los contenedores aunque los puertos estén "abiertos".

## 5. Latencia en Red Bridge
La red bridge añade una pequeña capa de virtualización (NAT). 
- **Problema:** En aplicaciones que requieren microsegundos (High Frequency Trading), este lag es inaceptable.
- **Solución:** Usa el driver `host` para eliminar la capa de red virtual de Docker.

## Resumen: Debug Step-by-Step
1. ¿Están en la misma red?
2. ¿Escucha la App en 0.0.0.0?
3. ¿El puerto del contenedor coincide con el del código?
4. ¿Tengo conectividad básica (ping/curl)?
Si respondes SÍ a todo, el problema está en tu código, no en Docker.
