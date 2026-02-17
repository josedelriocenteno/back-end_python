# Invalidación de Caché: El problema difícil

"Solo hay dos cosas difíciles en Ciencias de la Computación: la invalidación de caché, nombrar cosas y los errores por uno". (Phil Karlton).

## 1. ¿Por qué es difícil?
Si guardas el precio de un producto en caché y el dueño de la tienda lo cambia en la base de datos, tu caché ahora tiene un **dato mentiroso** (Stale Data). Debes decidir cuándo y cómo borrar la versión vieja.

## 2. Estrategias de Invalidación

### A. Basada en Tiempo (TTL)
La más sencilla. El dato "muere" solo después de X minutos.
*   **Problema:** Durante esos X minutos, el usuario verá datos viejos.

### B. Invalidación Activa (Purge)
Cuando cambia el dato en la DB, la propia aplicación lanza un comando a Redis para borrar esa clave específica: `r.delete(f"product:{id}")`.
*   **Problema:** Si tienes muchos sitios cambiando datos, es fácil que se te olvide invalidar alguno.

### C. Versionado de Claves
En lugar de borrar, cambias el nombre de la clave: `user_profile_v1` -> `user_profile_v2`.
*   Los usuarios nuevos pedirán la `v2` y la `v1` acabará muriendo por TTL.

## 3. Políticas de Desalojo (Eviction Policies)
¿Qué pasa si la memoria RAM de Redis se llena? Debe borrar cosas para dejar sitio a lo nuevo.
*   **LRU (Least Recently Used):** Borra lo que lleva más tiempo sin consultarse (nuestra favorita).
*   **LFU (Least Frequently Used):** Borra lo que se consulta pocas veces.
*   **Random:** Borra al azar (peligroso).

## 4. El peligro de la "Tormenta de Caché" (Thundering Herd)
Ocurre cuando una clave muy popular caduca (TTL muere) y de repente 10.000 usuarios intentan consultar la base de datos a la vez porque la caché está vacía.
*   **Solución:** Usar bloqueos (mutex) para que solo un proceso vaya a la DB y rellene la caché mientras los demás esperan unos milisegundos.

## 5. El impacto en la Experiencia de Usuario
La invalidación es un compromiso entre **Fresco** (siempre real) y **Rápido** (siempre caché). Tienes que preguntar al negocio: "¿Pasa algo si el usuario tarda 30 segundos en ver su cambio de foto de perfil?". Si la respuesta es "no", usa TTLs generosos para ganar rendimiento.

## Resumen: Coherencia y Control
Gestionar la caché no es solo guardar datos; es saber cuándo tirarlos a la basura. Un diseño profesional de caché incluye siempre una estrategia clara de mantenimiento para evitar que el sistema sirva información obsoleta o incorrecta.
