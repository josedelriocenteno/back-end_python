# OpenAPI y FastAPI: Documentación como Código

OpenAPI (anteriormente Swagger) es el lenguaje estándar para describir servicios REST. Una de las razones del éxito de FastAPI es que utiliza este estándar de forma nativa y automática.

## 1. El archivo `openapi.json`
FastAPI genera dinámicamente un archivo JSON que describe toda tu API:
*   Rutas y métodos.
*   Parámetros de entrada (Path, Query, Body).
*   Modelos de respuesta.
*   Esquemas de seguridad.
Puedes verlo en `http://localhost:8000/openapi.json`.

## 2. Swagger UI vs ReDoc
FastAPI ofrece dos interfaces visuales por defecto:
*   **Swagger UI (`/docs`):** Interactiva. Permite probar los endpoints directamente desde el navegador haciendo clic en "Try it out".
*   **ReDoc (`/redoc`):** Más limpia y profesional, ideal para lectura estructurada, aunque no permite ejecución de pruebas.

## 3. Metadata del Proyecto
Personaliza la información general en la instancia principal:
```python
app = FastAPI(
    title="Sistema de Gestión de Almacén",
    description="API de alto rendimiento para el control de stock en tiempo real.",
    version="2.4.1",
    terms_of_service="https://miempresa.com/terms/",
    contact={
        "name": "Equipo de Backend",
        "url": "https://miempresa.com/support",
        "email": "dev@miempresa.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
```

## 4. Tags: Organizando el Caos
Usa tags para agrupar endpoints relacionados. Swagger creará secciones visuales.
```python
@app.get("/users/", tags=["Gestión de Usuarios"])
def get_users(): ...

@app.get("/items/", tags=["Inventario"])
def get_items(): ...
```

## 5. Metadata por Endpoint
Puedes añadir detalles específicos a cada función:
*   **summary:** Título corto.
*   **description:** Explicación larga (puedes usar Markdown).
*   **response_description:** Qué significa el éxito de esta operación.

## Resumen: La API es el Contrato
Tu documentación no es algo que escribes *después* del código; es algo que nace *con* el código. Una documentación bien configurada reduce las dudas del equipo de frontend y sirve como la "verdad única" de cómo debe funcionar el sistema.
