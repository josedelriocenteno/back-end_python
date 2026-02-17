# Comparativa: ORM vs SQL Puro (Psycopg)

A menudo se presenta como una guerra de "uno u otro", pero en proyectos profesionales conviven ambos. Aquí tienes la comparativa técnica definitiva.

## 1. Cuadro Comparativo

| Característica | ORM (SQLAlchemy ORM) | SQL Puro (Psycopg3) |
| :--- | :--- | :--- |
| **Velocidad de Desarrollo** | Alta (Abstracción) | Media (Más código manual) |
| **Rendimiento (CPU/RAM)** | Menor (Capa de traducción) | Máximo (Cerca del metal) |
| **Mantenibilidad** | Alta (Refactorización fácil) | Media (Strings propensos a errores) |
| **Seguridad (SQLi)** | Alta (Protección nativa) | Alta (Si usas parámetros) |
| **Curva de Aprendizaje** | Alta (Muchos conceptos) | Baja (Si ya sabes SQL) |
| **Portabilidad (DB)** | Alta (Dialectos automáticos) | Baja (Sintaxis específica) |

## 2. Puntos Fuertes del ORM

1.  **Validación y Tipado:** Al usar clases de Python, tienes validación antes de tocar la DB.
2.  **Productividad en CRUD:** Crear, leer, actualizar y borrar registros simples es extremadamente rápido de escribir.
3.  **Gestión de Sesiones:** El *Identity Map* asegura que no tengas el mismo registro cargado dos veces con valores distintos en memoria.
4.  **Relaciones Transparentes:** Navegar de `usuario.perfil.direccion` es trivial.

## 3. Puntos Fuertes del SQL Puro

1.  **Transparencia Total:** Sabes exactamente qué query se está ejecutando.
2.  **Optimización Extrema:** Puedes usar `INDEX HINTS`, funciones específicas de Postgres o queries recursivas que el ORM no soporta bien.
3.  **Operaciones Masivas:** Insertar 1 millón de filas con `COPY` o `executemany` es órdenes de magnitud más rápido que crear 1 millón de objetos ORM.
4.  **Cero dependencias pesadas:** Ideal para micro-scripts o lambdas donde el tamaño del paquete importa.

## 4. El "Híbrido": SQLAlchemy Core

SQLAlchemy Core es el punto medio perfecto. Ofrece la seguridad y portabilidad del ORM pero con la velocidad y control del SQL puro. No mapea a objetos, mapea a tuplas rápidas.

## Resumen: Cuándo elegir qué

*   **Usa ORM para:** Aplicaciones web transaccionales, APIs CRUD, gestión de usuarios, lógica de negocio compleja.
*   **Usa SQL Puro para:** ETLs, reportes analíticos masivos, integración con bases de datos legacy, optimización de cuellos de botella.
*   **Tip Senior:** Si una query del ORM ocupa 50 líneas de Python y no se entiende, escríbela en SQL puro. La legibilidad manda.
