# Idempotencia: Por qué tu API no debe repetir acciones

La **Idempotencia** es la propiedad de algunas operaciones de dar el mismo resultado sin importar cuántas veces se ejecuten. En redes inestables (como internet móvil), es una garantía de seguridad crítica.

## 1. El Escenario de Desastre
El usuario pulsa el botón de "Comprar". La petición llega al servidor, se procesa el pago, pero la conexión se corta justo antes de que el servidor envíe la respuesta.
*   Si el usuario pulsa "Comprar" otra vez y tu API no es idempotente: **¡Cobrarás dos veces!**

## 2. Idempotencia según el Método HTTP

| Método | ¿Es Idempotente? | Por qué |
| :--- | :--- | :--- |
| **GET** | Sí | Leer los datos 10 veces no los cambia. |
| **PUT** | Sí | Sustituir el recurso por el mismo dato siempre resulta en ese dato. |
| **DELETE** | Sí | Borrar algo que ya no existe da el mismo resultado: nada. |
| **PATCH** | Generalmente no | Depende de la implementación (ej: `age = age + 1`). |
| **POST** | **NO** | Cada ejecución suele crear un recurso nuevo (ID diferente). |

## 3. Cómo hacer Idempotente un POST (Idempotency-Key)

Para procesos críticos (como pagos o creación de pedidos), se usa un header especial: `Idempotency-Key`.

1.  El cliente genera un UUID único para la transacción y lo envía en el Header.
2.  El servidor guarda ese UUID en una cache (Redis) por una ventana de tiempo (ej: 24h).
3.  Si llega otro POST con el **mismo UUID**, el servidor no ejecuta el proceso, sino que devuelve la respuesta que tenía guardada.

## 4. Idempotencia y Reintentos (Retries)
En arquitecturas de microservicios, los clientes suelen tener políticas de reintento automático. Tu API debe estar preparada para recibir la misma petición dos veces "por error" sin corromper el estado del sistema.

## 5. Diseño Defensivo
Incluso sin headers, puedes buscar duplicados lógicamente:
*   "No crees una orden si ya existe una orden activa con estos mismos items de este mismo usuario hace menos de 10 segundos".

## Resumen: Fiabilidad en el Mundo Real
Internet falla. Los navegadores se refrescan. Las apps se cierran. Diseñar para la idempotencia es lo que separa a una API de juguete de una API financiera o empresarial robusta.
