# Modelado Backend: Aplicación a Casos Reales

El modelado de datos no ocurre en el vacío. Depende totalmente de las necesidades de negocio y de cómo tu aplicación Python va a consumir esos datos. Aquí analizamos patrones avanzados para sistemas backend modernos.

## 1. Patrones de Identificadores (PKs)

### IDs Incrementales (SERIAL/BIGSERIAL)
*   **Pros:** Índices pequeños, orden natural, intuitivos.
*   **Contras:** Exponen volumen de datos (ej: `user_id=10` significa que eres de los primeros), problemas en bases de datos distribuidas.

### UUIDs (v4)
*   **Pros:** Imposibles de adivinar, únicos globalmente, perfectos para sistemas distribuidos (Microservicios).
*   **Contras:** Índices más grandes (16 bytes vs 4/8), dificultan la depuración visual.
*   *Recomendación:* Úsalos por defecto en aplicaciones web modernas.

## 2. Manejo de Estados e Históricos

### El Patrón de Estados
En lugar de un simple booleano `is_active`, usa un campo `status` y quizás una tabla `status_history`.
*   **Por qué:** Para auditoría. Necesitas saber *cuándo* y *por qué* un pedido pasó de "Pendiente" a "Cancelado".

### Versionado de Registros (Archiving)
Si necesitas mantener versiones antiguas de un documento (ej: términos de servicio):
*   **Opción A:** Tabla de históricos (`document_history`).
*   **Opción B:** Flag `is_current` y fecha de validez.

## 3. Modelado para Búsquedas

### EAV (Entity-Attribute-Value)
Usado cuando tienes entidades con atributos muy variables (ej: una tienda que vende desde ropa hasta componentes electrónicos).
*   *Tabla:* `entity_id`, `attribute_name`, `value`.
*   **CUIDADO:** EAV es un anti-patrón de rendimiento. Si usas PostgreSQL, **prefiere una columna JSONB**.

### JSONB en PostgreSQL: El Híbrido Perfecto
En lugar de complejas relaciones para datos variables, usa una columna JSONB para los "metadatos".
*   *Queries:* `SELECT * FROM products WHERE metadata->>'color' = 'red';`
*   *Ventaja:* Flexibilidad total sin sacrificar todas las bondades de SQL.

## 4. Herencia en Bases de Datos Relacionales

¿Cómo modelamos una clase `Vehiculo` de la que heredan `Coche` y `Moto`?

1.  **Table per Hierarchy:** Una sola tabla `vehiculos` con todas las columnas de todos los hijos y una columna `type`. (Muchos NULLs).
2.  **Table per Type:** Tabla `vehiculos` para datos comunes y tablas `coches`, `motos` vinculadas por FK para datos específicos. (Más JOINs, más limpio).
3.  **Table per Concrete Class:** Una tabla para `coches` y otra para `motos`. No hay tabla padre. (Dificulta consultas globales).

*Decisión:* Para Python/SQLAlchemy, **Table per Type** suele ser la más equilibrada.

## 5. El Impacto del Diseño en el Código (ORM vs SQL)

*   **SQLAlchemy / Django ORM:** Estos frameworks facilitan el modelado pero pueden ocultar ineficiencias (N+1 queries).
*   **Data Integrity:** Nunca dependas solo del ORM para la integridad. Define tus `UNIQUE`, `NOT NULL` y `FOREIGN KEY` siempre en la base de datos.
*   **Migrations:** Usa herramientas como Alembic para que tu modelado evolucione de forma controlada junto con tu código Python.

## Resumen: Checklist de Modelado Profesional

1.  [ ] ¿He elegido el tipo de ID correcto?
2.  [ ] ¿He normalizado hasta 3NF?
3.  [ ] ¿He identificado las relaciones (1:N, N:M)?
4.  [ ] ¿He usado `TIMESTAMPTZ` para auditoría?
5.  [ ] ¿He considerado el uso de JSONB para datos variables?
6.  [ ] ¿Mi diseño soporta el escalado futuro?
