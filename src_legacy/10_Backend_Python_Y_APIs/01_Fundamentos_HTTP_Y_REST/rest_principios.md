# Principios de REST (REpresentational State Transfer)

REST no es un protocolo, sino un **estilo arquitectónico**. Fue definido por Roy Fielding en su tesis doctoral y se ha convertido en el estándar de oro para las APIs modernas por su simplicidad y alineación con el protocolo HTTP.

## 1. Los 6 Constraints de REST

Para que una API sea considerada "RESTful", debe cumplir estas reglas:

1.  **Client-Server:** Separación total entre la interfaz de usuario y el almacenamiento de datos.
2.  **Stateless:** El servidor no guarda sesiones. Cada petición es independiente y autosuficiente.
3.  **Cacheable:** Las respuestas deben definirse como cacheables para mejorar el rendimiento.
4.  **Uniform Interface:** (El más importante) Todas las peticiones deben verse igual, sin importar quién las haga.
5.  **Layered System:** Un cliente no sabe si está conectado directamente al servidor final o a un intermediario (como un balanceador de carga).
6.  **Code on Demand (Opcional):** El servidor puede enviar código ejecutable (como JavaScript) al cliente.

## 2. El Recurso: El Atomo de REST
En REST, todo es un **Recurso**. Un recurso se identifica por su URI (Uniform Resource Identifier).
*   **Ejemplo:** `/users/42`
*   No navegamos por páginas, sino por recursos y sus relaciones.

## 3. Naming y Convenciones Profesionales

Una API REST profesional sigue reglas de nomenclatura estrictas:

*   **Usa Sustantivos Plurales:** `/products` en lugar de `/get_product`.
*   **Usa Jerarquía para Relaciones:** `/users/10/orders` para indicar "los pedidos del usuario 10".
*   **Usa Kebab-case en URLs:** `/user-profiles` en lugar de `/userProfiles`.
*   **Evita verbos en la URL:** `/create-user` es un error; usa `POST /users`.

## 4. Richardson Maturity Model: Los Niveles de REST

¿Qué tan RESTful es tu API?
*   **Nivel 0 (The Swamp of POX):** Usas HTTP solo como medio de transporte (ej: SOAP). Una sola URL para todo.
*   **Nivel 1 (Resources):** Empiezas a usar nombres de recursos individuales.
*   **Nivel 2 (HTTP Verbs):** Usas los métodos GET, POST, DELETE correctamente. (Aquí está el 90% de las APIs actuales).
*   **Nivel 3 (HATEOAS):** La respuesta incluye enlaces a otras acciones posibles. (El "Santo Grial" de REST).

## 5. Por qué REST ha ganado
REST es predecible. Si conozco el recurso (`/users`), sé que:
*   `GET /users` -> Lista.
*   `POST /users` -> Crear.
*   `GET /users/5` -> Detalles de uno.

## Resumen: Simplicidad que Escala

REST aprovecha al máximo la infraestructura de internet. Al ser Stateless y Resource-based, permite que los desarrolladores frontend y backend trabajen en paralelo con un contrato claro y predecible.
