# REST vs RPC (vs GraphQL): Eligiendo la Arquitectura

REST no es la única forma de conectar sistemas. Dependiendo de tu caso de uso, podrías beneficiarte de otros estilos.

## 1. RPC (Remote Procedure Call)
En lugar de manipular recursos, llamas a "funciones remotas" como si fueran locales.
*   **Estilo:** `/createUser`, `/calculatePrice`.
*   **gRPC (Moderno):** Desarrollado por Google. Usa Protobuf (binario) y HTTP/2. Es muchísimo más rápido que REST pero menos amigable para navegadores.
*   **Cuándo usarlo:** Comunicación interna de Microservicios donde la latencia es crítica.

## 2. GraphQL
En lugar de tener muchos endpoints, tienes **uno solo**. El cliente envía una consulta pidiendo exactamente qué campos quiere.
*   **Estilo:** El cliente dice: "Dame el usuario 1, pero solo su nombre y sus últimos 2 posts".
*   **Ventaja:** Evita el *Over-fetching* (traer más datos de los necesarios).
*   **Cuándo usarlo:** Frontends complejos (como el de Facebook o GitHub) que necesitan datos de muchas tablas distintas a la vez.

## 3. Comparativa Técnica

| Característica | REST | RPC (gRPC) | GraphQL |
| :--- | :--- | :--- | :--- |
| **Abstracción** | Recurso (Sustantivo) | Procedimiento (Verbo) | Grafo de Datos |
| **Payload** | JSON (Legible) | Binario (Compacto) | JSON con Query |
| **Velocidad** | Media | Muy Alta | Media (Post-procesado) |
| **Tipado** | Débil (OpenAPI) | Fuerte (Protobuf) | Fuerte (Schema) |

## 4. El Veredicto: El "Go-To" es REST
REST sigue siendo el estándar porque:
1.  **Es fácil de cachear:** Los navegadores entienden GET.
2.  **Es fácil de debugear:** Solo necesitas un navegador para probarlo.
3.  **Ubicuidad:** El 99% de las librerías de todos los lenguajes soportan REST perfectamente.

## Resumen: La herramienta adecuada
*   **REST:** Para APIs públicas y comunicación web estándar.
*   **gRPC:** Para backend-to-backend de alto rendimiento.
*   **GraphQL:** Para frontends dinámicos que cambian sus requisitos de datos constantemente.

En este curso nos centraremos en REST por ser la base fundamental del desarrollo Web moderno.
