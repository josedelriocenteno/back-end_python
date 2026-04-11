# Versionado de Documentación: Evitando el Caos

A medida que tu API evoluciona hacia la V2, la V3, etc., tu documentación debe reflejar estos cambios sin que los usuarios de versiones anteriores se pierdan.

## 1. Documentación por Versión (Ruta)
La forma más limpia en FastAPI es tener un punto de entrada Swagger diferente para cada router:

```python
# app/main.py
app = FastAPI()

app.include_router(api_v1_router, prefix="/v1", tags=["API V1"])
app.include_router(api_v2_router, prefix="/v2", tags=["API V2"])
```
En Swagger verás bloques separados. El usuario simplemente hace scroll hasta la versión que le interesa.

## 2. Changelog dentro de la API
Es una gran práctica incluir una sección de "Novedades" o "Cambios recientes" en la descripción principal de la app:
```python
description = """
**Versión 2.0.0 (Actual)**
- Cambio en el esquema de respuesta de /search.
- Añadida autenticación 2FA.

**Versión 1.5.0**
- Soporte para exportación a CSV.
"""
```

## 3. El Header `Deprecated` en OpenAPI
Puedes marcar endpoints como obsoletos directamente en el código. Swagger los mostrará tachados o con un aviso visual de "Deprecated".

```python
@app.get("/old-path", deprecated=True)
def old_function():
    return {"message": "Usa /new-path en su lugar"}
```

## 4. Documentación de Esquemas de Seguridad
Si cambias de OAuth2 a JWT simple o a una API Key, la documentación debe reflejar cómo autenticarse de forma clara para cada caso.

## 5. Exportación de Contratos
A veces los equipos necesitan el archivo `openapi.json` offline. Puedes crear un script que exporte la documentación cada vez que haya un commit:
```bash
# Simulado
python -c "import json; from app.main import app; print(json.dumps(app.openapi()))" > openapi_contract.json
```

## Resumen: Sincronía Total
La peor pesadilla de un desarrollador es una documentación que dice una cosa y una API que hace otra. Gestionar el versionado de la documentación con el mismo rigor que el del código es lo que distingue a una empresa tecnológica madura.
