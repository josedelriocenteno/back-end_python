# Docstrings y su impacto en la API

En la mayoría de los lenguajes, los comentarios son solo explicaciones para humanos. En FastAPI, los **Docstrings** se convierten automáticamente en la descripción de los endpoints en Swagger.

## 1. El Docstring de la Función
FastAPI toma la primera línea del docstring como el `summary` y el resto como la `description`.

```python
@app.post("/process-data")
def process_data():
    """
    Procesa un lote de datos masivo. # Esto es el summary
    
    Este endpoint se encarga de recibir un CSV, validar cada fila y 
    guardarlo en la base de datos de producción. 
    **Nota:** Tarda aproximadamente 2 segundos. # Esto es la description
    """
    ...
```

## 2. Soporte para Markdown
La descripción de los endpoints en Swagger soporta Markdown completo. Úsalo para mejorar la legibilidad:
*   **Negritas** para advertencias.
*   `Código` para nombres de campos o variables.
*   Listas para explicar diferentes casos de uso.
*   Enlaces a documentación externa o Jira.

## 3. Documentando Esquemas (Pydantic)
Los docstrings en las clases de Pydantic también se capturan:

```python
class Token(BaseModel):
    """
    Esquema para la entrega de tokens JWT tras un login exitoso.
    """
    access_token: str
    token_type: str = "bearer"
```

## 4. Por qué es mejor que los comentarios estándar
1.  **Visibilidad:** El desarrollador que usa tu API no tiene que abrir tu código Python para saber qué hace la función.
2.  **Mantenibilidad:** Obliga al programador a mantener la documentación cerca del código.
3.  **Profesionalidad:** Una API con descripciones detalladas transmite confianza y reduce el tiempo de integración.

## 5. El principio de "Auto-Documentación"
Aprovecha los nombres de los argumentos y los tipos:
*   `def delete_user(user_id: int):` Ya es bastante informativa.
*   `def delete_user(user_id: Annotated[int, "ID del usuario a borrar"]):` Es perfecta.

## Resumen: Escribe para los demás
Tu "yo del futuro" y tus compañeros de equipo te agradecerán que cada endpoint tenga un docstring claro. No expliques *cómo* funciona el código (eso se lee en el código), explica *qué* hace el endpoint y *por qué* existe.
