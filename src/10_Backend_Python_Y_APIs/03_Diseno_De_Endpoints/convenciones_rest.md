# Convenciones REST y Naming Limpio

Un endpoint no es solo una dirección; es parte de un lenguaje. El naming profesional hace que tu API sea "auto-explicativa" (Self-documenting).

## 1. Reglas de Oro de Naming

*   **Sustantivos, no verbos:**
    *   MAL: `GET /get_active_users`
    *   BIEN: `GET /users?status=active`
*   **Plurales siempre:**
    *   MAL: `/user/10`
    *   BIEN: `/users/10` (Es el décimo elemento de la colección "usuarios").
*   **Kebab-case para URLs:**
    *   MAL: `/order_details/` o `/order_Details/`
    *   BIEN: `/order-details/`

## 2. Estructura de Recursos Jerárquicos

Indica pertenencia de forma natural:
*   `GET /authors/4/books` -> Los libros del autor 4.
*   `POST /authors/4/books` -> Añadir un libro a ese autor.

**Evita la sobre-anidación:**
*   MAL: `/authors/4/books/12/chapters/1/paragraphs/5`
*   BIEN: `/paragraphs/5` (A menos que el párrafo no tenga sentido sin el contexto del autor y el libro). Una regla común es no pasar de 2 o 3 niveles.

## 3. Query Strings vs Path Params
*   **Path Param:** Para identificar **un recurso** (`id`, `uuid`, `slug`). Obligatorio.
*   **Query String:** Para **modificar la vista** de los recursos (`limit`, `sort`, `filter`). Opcional.

## 4. Respuestas Consistentes

Si tu API devuelve errores, todos deben tener la misma estructura:
```json
{
  "error": "Not Found",
  "message": "El usuario con ID 99 no existe",
  "code": "USR_001"
}
```
Esto permite que los desarrolladores frontend creen manejadores de errores universales.

## 5. El uso de trailing slashes
FastAPI es estricto por defecto. `/users` y `/users/` son rutas distintas.
*   **Convención:** Mantén una consistencia en todo el proyecto. La mayoría de las APIs modernas prefieren NO usar el slash final (`/users`).

## Resumen: Código que se Lee como un Libro
Si un desarrollador nuevo entra en tu proyecto y puede adivinar la URL de un recurso antes de mirar la documentación, has hecho un gran trabajo de naming.
