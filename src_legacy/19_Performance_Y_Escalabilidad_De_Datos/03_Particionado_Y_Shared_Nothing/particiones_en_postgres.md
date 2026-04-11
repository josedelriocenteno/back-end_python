# Particiones en PostgreSQL: Métodos y Sintaxis

Desde la versión 10, PostgreSQL soporta particionado declarativo, facilitando enormemente su implementación. Vamos a ver los 3 métodos principales.

## 1. Range Partitioning (Por Rangos)
Ideal para fechas o valores numéricos secuenciales.
```sql
CREATE TABLE facturas (
    id int,
    fecha date not null,
    total decimal
) PARTITION BY RANGE (fecha);

-- Creamos las particiones reales
CREATE TABLE facturas_2023 PARTITION OF facturas
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE facturas_2024 PARTITION OF facturas
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

## 2. List Partitioning (Por Lista)
Ideal para categorías discretas, como regiones o estados.
```sql
CREATE TABLE clientes (
    id int,
    nombre text,
    pais text
) PARTITION BY LIST (pais);

CREATE TABLE clientes_espana PARTITION OF clientes
    FOR VALUES IN ('España');

CREATE TABLE clientes_resto_europa PARTITION OF clientes
    FOR VALUES IN ('Francia', 'Portugal', 'Italia');
```

## 3. Hash Partitioning (Por Hash)
Ideal para repartir la carga de forma uniforme cuando no hay un rango o lista clara.
```sql
CREATE TABLE usuarios (
    id int,
    username text
) PARTITION BY HASH (id);

-- Creamos 4 particiones para repartir los usuarios
CREATE TABLE usuarios_p0 PARTITION OF usuarios FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE usuarios_p1 PARTITION OF usuarios FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE usuarios_p2 PARTITION OF usuarios FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE usuarios_p3 PARTITION OF usuarios FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

## 4. La partición DEFAULT
Es una buena práctica crear una partición por defecto para capturar datos que no encajen en ninguna de las otras reglas, evitando así que la inserción de datos falle.
```sql
CREATE TABLE facturas_default PARTITION OF facturas DEFAULT;
```

## 5. El papel de la Clave de Partición
La clave de partición **debe estar incluida** en cualquier restricción de unicidad (`UNIQUE` o `PRIMARY KEY`). No puedes tener una PK solo en `id` si particionas por `fecha` en Postgres; la PK debe ser `(id, fecha)`.

## Resumen: Implementación Nativa
PostgreSQL ofrece herramientas potentes para organizar tus datos físicamente. Elegir el método de particionado correcto (Rango, Lista o Hash) es el primer paso para asegurar que tu base de datos relacional pueda seguir creciendo sin degradar el rendimiento.
