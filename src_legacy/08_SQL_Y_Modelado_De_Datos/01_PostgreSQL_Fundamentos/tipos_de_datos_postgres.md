📘 tipos_de_datos_postgres.md
int, text, jsonb, uuid (y por qué elegir bien importa más de lo que crees)
1. Por qué los tipos de datos sí importan

Muchos principiantes creen que los tipos de datos son un detalle menor.
Error grave.

Elegir bien un tipo de dato afecta directamente a:

✔️ Integridad de los datos (evitar datos inválidos)

✔️ Rendimiento (índices, búsquedas, joins)

✔️ Uso de memoria y disco

✔️ Facilidad de evolución del sistema

✔️ Bugs silenciosos en backend y data

PostgreSQL es potente porque tiene muchos tipos, no porque tenga pocos.

2. Categorías mentales básicas (antes de entrar en tipos concretos)

Antes de memorizar nombres, entiende esto:

Categoría	Pregunta clave
Numéricos	¿Se calcula con ello?
Texto	¿Es solo información legible?
Identificadores	¿Identifica de forma única?
Estructurados	¿Tiene forma interna (JSON)?
Temporales	¿Depende del tiempo?

En este archivo nos centramos en:

int

text

jsonb

uuid

Porque cubren el 80% de sistemas reales.

3. int — números enteros (pero no todos son iguales)
3.1 Qué es int

int (realmente integer) representa números enteros:

Sin decimales

Positivos y negativos

Ejemplos:

IDs numéricos

Contadores

Edades

Cantidades discretas

3.2 Variantes de enteros en PostgreSQL
Tipo	Tamaño	Rango aproximado
smallint	2 bytes	±32 mil
integer (int)	4 bytes	±2 mil millones
bigint	8 bytes	enorme

👉 Regla práctica:

Usa integer por defecto

Usa bigint solo si sabes que crecerá mucho

No optimices prematuramente

3.3 Cuándo NO usar int

❌ Para teléfonos
❌ Para códigos postales
❌ Para números con ceros a la izquierda
❌ Para identificadores públicos

¿Por qué?
Porque no son números, son texto disfrazado.

4. text — el comodín (y sus trampas)
4.1 Qué es text

text es una cadena de caracteres de longitud variable.

PostgreSQL no limita el tamaño (salvo por memoria).

Ejemplos típicos:

Nombres

Emails

Descripciones

URLs

Mensajes

4.2 text vs varchar

En PostgreSQL:

text y varchar rinden igual

La diferencia es semántica, no técnica.

Tipo	Uso recomendado
text	Casi siempre
varchar(n)	Cuando el límite es una regla de negocio

👉 Regla profesional:
Usa text + CHECK si necesitas validación real.

4.3 Trampa clásica con text

Usar text para todo:

id TEXT


Esto:

❌ rompe índices

❌ complica joins

❌ permite basura

❌ hace lento el sistema

text no es un sustituto universal.

5. uuid — identificadores modernos y serios
5.1 Qué es un UUID

UUID = Universally Unique Identifier

Ejemplo:

550e8400-e29b-41d4-a716-446655440000


No es legible.
No es secuencial.
Pero es único globalmente.

5.2 Cuándo usar uuid

Usa uuid cuando:

Hay microservicios

Hay APIs públicas

Hay datos distribuidos

No quieres exponer IDs secuenciales

Generas IDs fuera de la BD

Ejemplo típico:

Backend moderno

Apps móviles

Sistemas cloud

5.3 UUID vs INT (comparación honesta)
Aspecto	int	uuid
Legible	✔️	❌
Secuencial	✔️	❌
Seguro públicamente	❌	✔️
Distribuido	❌	✔️
Tamaño	pequeño	mayor

👉 Conclusión:

Backend simple → int

Backend moderno/distribuido → uuid

6. jsonb — SQL + NoSQL bien hecho
6.1 Qué es jsonb

jsonb es JSON binario, no texto.

PostgreSQL:

Lo parsea

Lo valida

Lo indexa

Lo consulta eficientemente

NO es lo mismo que json.

6.2 Cuándo usar jsonb

Usa jsonb cuando:

La estructura varía

No merece una tabla propia

Los campos cambian con el tiempo

Necesitas flexibilidad

Ejemplos reales:

Configuraciones

Metadata

Preferencias de usuario

Payloads de APIs externas

6.3 Cuándo NO usar jsonb

❌ Para datos relacionales
❌ Para joins frecuentes
❌ Para datos críticos
❌ Para evitar modelar bien

jsonb no sustituye el modelado relacional.

7. Combinaciones reales (cómo se usan juntos)

Ejemplo típico profesional:

id UUID PRIMARY KEY,
email TEXT NOT NULL,
edad INTEGER,
preferencias JSONB,
created_at TIMESTAMP


Aquí:

uuid identifica

text comunica

int calcula

jsonb flexibiliza

Esto no es casualidad.

8. Errores comunes que debes evitar

❌ Usar text para IDs
❌ Usar int para cosas que no son números
❌ Meter todo en jsonb por pereza
❌ Elegir tipos “porque funcionan”
❌ Copiar esquemas sin entenderlos

9. Regla de oro (memorízala)

El tipo de dato expresa intención, no solo almacenamiento

Si el tipo es incorrecto:

El esquema miente

El código se complica

Los bugs aparecen tarde

El rendimiento sufre

10. Lo que viene después

Con esto claro, ahora sí tiene sentido:

Crear tablas bien (create_table.sql)

Definir constraints

Modelar relaciones

Pensar en índices