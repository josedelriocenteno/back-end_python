# Arquitectura de la Capa de Acceso a Datos

En aplicaciones pequeñas, es común ver queries de SQL mezcladas con la lógica de las rutas (API). En aplicaciones profesionales (Enterprise), esto es una receta para el desastre. Necesitamos una **Capa de Persistencia** bien definida.

## 1. El Patrón de Capas (Layered Architecture)

Una estructura típica de Backend se divide así:

1.  **Capa de Presentación (Controladores/Rutas):** Recibe HTTP, valida el JSON de entrada.
2.  **Capa de Negocio (Servicios):** Contiene las reglas (ej: "un usuario no puede comprar si no tiene saldo").
3.  **Capa de Persistencia (Acceso a Datos):** El único lugar donde se habla con la base de datos (SQL/ORM).
4.  **Capa de Datos (Infraestructura):** La base de datos física (PostgreSQL, Redis).

## 2. Abstracciones Comunes

Para separar la lógica de negocio de la base de datos, usamos patrones como:

*   **Repository Pattern:** Una interfaz que expone métodos como `get_user_by_id(user_id)` en lugar de exponer la sesión de la DB.
*   **Unit of Work:** Gestiona las transacciones para asegurar que varias operaciones en diferentes repositorios ocurran "todo o nada".
*   **DAO (Data Access Object):** Similar al repositorio pero más enfocado a la tabla que a la entidad de negocio.

## 3. ¿Por qué separar el Acceso a Datos?

1.  **Testeabilidad:** Puedes "mockear" (simular) la base de datos en tus tests de lógica de negocio sin necesitar una DB real.
2.  **Mantenibilidad:** Si decides cambiar de PostgreSQL a MySQL (o de SQLAlchemy a Tortoise), solo tocas la capa de persistencia, no tus 50 servicios.
3.  **Legibilidad:** Tus servicios se centran en el *qué* ("Crear pedido") y no en el *cómo* ("INSERT INTO orders...").

## 4. El Ciclo de Vida de la Conexión

Una arquitectura robusta debe gestionar:
*   **Pooling:** Reutilización de conexiones para evitar la latencia de apertura.
*   **Inyección de Dependencias:** Pasar la sesión de la DB a los servicios para que puedan trabajar de forma coordinada.
*   **Manejo Global de Transacciones:** Abrir la transacción al inicio del request y hacer commit al final (si todo fue bien).

## Resumen: Desacoplamiento es Poder

No dejes que tu base de datos dicte cómo escribes tu código Python. Al construir una arquitectura de capas, proteges tu lógica de negocio y aseguras que tu aplicación pueda crecer y evolucionar sin quedar atrapada en los detalles de implementación de tu motor SQL.
