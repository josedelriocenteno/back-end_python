# HTTP Básico: El Protocolo del Backend

HTTP (HyperText Transfer Protocol) es el lenguaje universal que permite la comunicación entre el cliente y el servidor. Como desarrollador backend, debes entender que HTTP no es solo "enviar texto", sino una estructura rica con reglas específicas.

## 1. El Modelo Request-Response

Toda comunicación HTTP comienza con una **Petición (Request)** del cliente y termina con una **Respuesta (Response)** del servidor.

### Elementos de una Petición:
*   **Método (Verbo):** Qué acción queremos realizar (GET, POST, etc).
*   **URL (Path):** Dónde está el recurso que buscamos.
*   **Headers:** Metadatos (Tipo de contenido, Autenticación, User-Agent).
*   **Body (Cuerpo):** Los datos reales (generalmente un JSON), presentes en POST/PUT/PATCH.

### Elementos de una Respuesta:
*   **Status Code:** El resultado numérico (200, 404, 500).
*   **Headers:** Información del servidor, tipo de respuesta, políticas de seguridad.
*   **Body:** El contenido devuelto (JSON, HTML, Imagen).

## 2. Los Verbos HTTP (Métodos)

Diseñar una API profesional significa usar el verbo correcto para cada acción:

| Método | Acción | ¿Tiene Body? | Uso Típico |
| :--- | :--- | :--- | :--- |
| **GET** | Leer | No | Obtener un usuario o una lista de productos. |
| **POST** | Crear | Sí | Registrar un nuevo usuario o procesar un pago. |
| **PUT** | Reemplazar | Sí | Actualizar TODO un recurso (cambiar todos los datos). |
| **PATCH** | Modificar | Sí | Actualizar SOLO un campo (ej: solo el email). |
| **DELETE** | Borrar | No | Eliminar un post o una cuenta. |

## 3. Headers Cruciales para Backend

*   **Content-Type:** `application/json` le dice al servidor que lo que viene es un JSON.
*   **Authorization:** Donde colocamos el Token JWT (`Bearer <token>`).
*   **Accept:** El cliente le dice al servidor qué tipo de respuesta espera.
*   **User-Agent:** Identifica qué dispositivo está llamando (útil para analítica).

## 4. Evolución: HTTP/1.1 vs HTTP/2 vs HTTP/3
*   **HTTP/1.1:** El estándar clásico. Una conexión por recurso (lento).
*   **HTTP/2:** Binario y multiplexado. Permite muchas peticiones por una sola conexión TCP.
*   **HTTP/3:** Usa el protocolo QUIC (UDP). Diseñado para máxima velocidad y evitar el bloqueo de cabeza de línea en redes inestables.

## Resumen: La Fundación de tu API

Sin HTTP, no hay internet. Dominar el flujo de cabeceras, métodos y cuerpos es el primer paso para construir sistemas interoperables. En el siguiente archivo, veremos cómo REST utiliza estas reglas para crear arquitecturas elegantes.
