# Inyección de Dependencias Asíncronas

FastAPI brilla por su sistema de inyección de dependencias (`Depends`). Lo que muchos no saben es que este sistema soporta asincronía de forma nativa y extremadamente potente.

## 1. La Dependencia Async
Tus dependencias pueden ser `async def`. FastAPI esperará a que terminen antes de llamar a tu endpoint.
- **Caso típico:** Obtener el usuario actual desde un token JWT consultando la DB.

```python
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db 
    finally:
        await db.close() # El teardown también es async!
```

## 2. Dependencias de Dependencias
Puedes encadenar dependencias asíncronas. FastAPI creará un "Grafo de Dependencias" y las ejecutará en el orden correcto, esperando cada `await` necesario.

## 3. Sub-dependencias Concurrentes
Si un endpoint tiene 5 dependencias asíncronas que no dependen entre sí, FastAPI es capaz de ejecutarlas de forma eficiente para que el tiempo total de espera sea el mínimo posible.

## 4. Yield y Recursos Asíncronos
El uso de `yield` en una dependencia asíncrona es la forma estándar de gestionar recursos que requieren limpieza, como conexiones de base de datos o sesiones HTTP. FastAPI garantiza que el bloque `finally` se ejecutará incluso si el endpoint lanza un error.

## 5. El coste de la inyección
FastAPI ha sido optimizado para que el coste de inyectar una dependencia sea despreciable. No tengas miedo de usarlas para modularizar tu lógica de seguridad y acceso a datos.

## Resumen: Código Desacoplado
Usar dependencias asíncronas te permite tener endpoints muy limpios:
`@app.get("/") async def index(user = Depends(get_user), db = Depends(get_db)): ...`
Toda la complejidad de la conexión y la autenticación queda oculta tras la inyección, manteniendo el motor `async` rindiendo al 100%.
