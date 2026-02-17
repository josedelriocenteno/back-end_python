# Serialización JSON: De Objeto a Texto

La serialización es el proceso de transformar una estructura de datos de Python (Objetos, Listas, Datetimes) en una cadena de texto JSON que pueda viajar por la red.

## 1. El reto de los tipos no estándar
JSON solo entiende de números, strings, booleanos, arrays y nulos. Sin embargo, en Backend usamos:
*   **Datetimes:** ¿Como `ISO-8601`? ¿Timestamp?
*   **Decimals:** Para dinero (evitando errores de punto flotante).
*   **UUIDs:** Para identificadores únicos.
*   **Enums:** Para estados (Active, Pending...).

## 2. Cómo lo soluciona FastAPI (Pydantic)
Pydantic tiene codificadores internos para casi todo:
*   Un `datetime` se convierte automáticamente a un string `"2023-10-27T10:00:00"`.
*   Un `UUID` se convierte a su representación hexadecimal.
*   Un `Enum` se convierte a su valor (`.value`).

## 3. Custom Encoders
Si tienes un tipo de datos propio, puedes enseñarle a Pydantic cómo serializarlo:
```python
class MyModel(BaseModel):
    my_data: MySpecialType

    model_config = {
        "json_encoders": {
            MySpecialType: lambda v: v.to_custom_string()
        }
    }
```

## 4. Aliases: Cambiando nombres en el JSON
A veces Python usa `snake_case` pero el frontend espera `camelCase`.
```python
class User(BaseModel):
    first_name: str = Field(alias="firstName")
    
    # Esto permite recibir/enviar 'firstName' en el JSON,
    # pero usar 'first_name' en tu código Python.
    model_config = {"populate_by_name": True}
```

## 5. Exclusión de Campos Dinámica
Puedes decidir qué campos enviar en el momento de la respuesta:
```python
return my_object.model_dump(exclude={"internal_notes", "secret_key"})
```

## Resumen: El lenguaje universal
El JSON es el contrato entre tu servidor y el mundo. Asegúrate de que sea limpio, predecible y que respete los estándares internacionales (ISO) para fechas y monedas. Entender la serialización te permite enviar exactamente lo que el cliente necesita, nada más y nada menos.
