# Versionado de Endpoints: Evolucionando sin romper nada

Una API exitosa siempre cambia. El desafío es cómo añadir nuevas funcionalidades o cambiar estructuras sin romper las aplicaciones móviles o integraciones de tus clientes que ya están usando la versión antigua.

## 1. ¿Por qué versionar?
*   **Breaking Changes:** Necesitas renombrar un campo de `username` a `handle`.
*   **Nueva Lógica:** El proceso de pago en la V2 requiere un paso extra que la V1 no tiene.
*   **Limpieza:** Quieres deshacerte de código antiguo pero no puedes obligar a todos los usuarios a actualizar su App móvil el mismo día.

## 2. Estrategia A: Versionado en la URL (Recomendado)
Es la más clara y fácil de debugear.
`https://api.miempresa.com/v1/users`
`https://api.miempresa.com/v2/users`

**Implementación en FastAPI:**
```python
from fastapi import FastAPI, APIRouter

router_v1 = APIRouter(prefix="/v1")
router_v2 = APIRouter(prefix="/v2")

app.include_router(router_v1)
app.include_router(router_v2)
```

## 3. Estrategia B: Versionado en Headers
El cliente envía un header como `Accept: application/vnd.myapi.v2+json`.
*   **Pros:** URL limpia.
*   **Contras:** Difícil de probar desde el navegador, mala visibilidad en logs de acceso.

## 4. Política de Deprecación (Deprecation)
Cuando lanzas una versión nueva:
1.  **Anuncio:** Notifica a los usuarios que la V1 se marcará como vieja.
2.  **Warning:** Añade el header `Deprecation` en las respuestas de la V1.
3.  **Sunset:** Define una fecha de apagado (`Sunset` header).
4.  **Apagado:** Solo cuando el tráfico en la V1 sea residual.

## 5. El "Forwarding" de Versiones
A veces, la V1 simplemente llama internamente a la V2 y transforma la respuesta para que parezca antigua. Esto ahorra mantener dos lógicas de negocio diferentes.

## Resumen: Respeto al Cliente
El programador senior entiende que una API es un contrato. El versionado es la forma de honrar ese contrato mientras el sistema sigue innovando. Siempre que sea posible, mantén la compatibilidad hacia atrás.
