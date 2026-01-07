📘 esquemas_y_roles.md
Organización y permisos en PostgreSQL (como se hace en sistemas reales)
1. El problema que este tema resuelve (contexto real)

Imagina esto:

Tienes varias tablas

Varios servicios

Varios desarrolladores

Entornos distintos (dev, staging, prod)

Preguntas críticas:

❓ ¿Quién puede leer qué?

❓ ¿Quién puede modificar qué?

❓ ¿Cómo evitas que alguien rompa todo?

❓ ¿Cómo organizas 200 tablas sin volverte loco?

👉 Esquemas y roles existen para esto.

2. Qué es un esquema (schema)
2.1 Definición simple

Un esquema es un namespace, un contenedor lógico dentro de una base de datos.

Piensa en:

Carpetas dentro de un proyecto

Paquetes en Python

Módulos en Java

Ejemplo conceptual:

base_de_datos
├── public
├── auth
├── billing
└── analytics


Todas están en la misma base de datos, pero organizadas.

2.2 El esquema public

PostgreSQL crea por defecto:

public


Todo lo que no especifiques va ahí.

❌ En proyectos reales no deberías dejar todo en public.

3. Por qué usar esquemas (beneficios reales)
3.1 Organización

Separar por dominio:

auth.users

billing.invoices

analytics.events

Evita:

Choques de nombres

Caos mental

Tablas “huérfanas”

3.2 Seguridad

Permites:

Acceso a unas tablas

Negar acceso a otras

Sin duplicar bases de datos.

3.3 Claridad semántica

Cuando ves:

analytics.events


ya sabes:

Para qué sirve

Quién la usa

Qué tocar (y qué no)

4. Qué es un rol (role)
4.1 Definición clara

Un rol es una identidad que puede:

Conectarse

Tener permisos

Heredar permisos

Representar:

Un usuario

Un servicio

Un grupo

En PostgreSQL:

usuarios y roles son lo mismo

4.2 Tipos mentales de roles
Tipo	Ejemplo
Humano	dev, admin
Servicio	api_backend
Grupo	read_only

Un rol puede representar una persona o un sistema.

5. Separación crítica: roles ≠ esquemas

Esto es importante:

Esquemas organizan objetos

Roles controlan acceso

Nunca los confundas.

6. Permisos básicos (sin comandos aún)

Antes de ver SQL, entiende los conceptos:

Permiso	Significa
CONNECT	Puede conectarse a la BD
USAGE	Puede usar un esquema
SELECT	Leer datos
INSERT	Insertar
UPDATE	Modificar
DELETE	Borrar
EXECUTE	Ejecutar funciones

Permisos no son globales, se aplican a:

Bases de datos

Esquemas

Tablas

Secuencias

Funciones

7. Esquemas en entornos reales
7.1 Backend típico
auth
core
billing
notifications


Cada microdominio en su esquema.

7.2 Data / Analytics
raw
staging
analytics


Flujo claro:

raw → staging → analytics

8. Error clásico de principiantes

❌ Un solo usuario “admin” para todo
❌ Todo en public
❌ Permisos por pereza
❌ Aplicación con permisos de superusuario

👉 Esto rompe seguridad y escalabilidad.

9. Patrón profesional mínimo (mental)

Aunque no veamos SQL aún, quédate con esto:

Un rol admin

Un rol app

Un rol read_only

Esquemas separados por dominio

La app no es dueña de todo

10. Por qué esto importa incluso si trabajas solo

Aunque seas tú solo:

Aprendes a pensar bien

Evitas malas prácticas

Tu proyecto escala

Tu mentalidad es profesional

11. Qué viene después

Con esquemas y roles claros, ahora sí tiene sentido:

Crear tablas (create_table.sql)

Definir constraints

Modelar relaciones reales

Pensar en seguridad desde el diseño

👉 El siguiente archivo:
create_table.sql
Aquí pasamos de teoría a SQL serio.