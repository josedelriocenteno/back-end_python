bases_datos_relacionales.md
Tablas, filas, columnas y relaciones (bien entendidas, no de memoria)
1. ¿Qué es una base de datos relacional?

Una base de datos relacional es un sistema para almacenar datos estructurados siguiendo el modelo relacional, propuesto por Edgar F. Codd en 1970.

La palabra clave aquí es modelo.

👉 No es solo “guardar datos”, es una forma concreta y rigurosa de organizarlos.

2. El modelo relacional (la idea base)

El modelo relacional se apoya en tres ideas fundamentales:

Los datos se almacenan en relaciones

Las relaciones se representan como tablas

Las relaciones entre datos se expresan mediante claves

Vamos a bajar esto a tierra.

3. Qué es una tabla (de verdad)

Una tabla representa una entidad del mundo real.

Ejemplos de entidades:

Usuario

Pedido

Producto

Cuenta bancaria

Evento

Sensor

Una tabla NO es:

Un fichero cualquiera

Un JSON gigante

Una lista sin reglas

Una tabla es una estructura estricta, con reglas claras.

Ejemplo conceptual: tabla usuarios
id	nombre	email	edad
1	Ana	ana@mail.com
	25
2	Luis	luis@mail.com
	31

Esta tabla representa la entidad Usuario.

4. Columnas: qué significan realmente

Cada columna representa un atributo de la entidad.

En el ejemplo:

id → identificador

nombre → nombre del usuario

email → correo electrónico

edad → edad

Pero ojo:
Una columna no es solo un nombre.

Cada columna tiene:

Un tipo de dato

Reglas

Restricciones

Ejemplo conceptual:

edad → entero, no negativo
email → texto, único
id → entero, no nulo


👉 Esto es lo que da consistencia a la base de datos.

5. Filas: instancias, no “registros sueltos”

Cada fila representa una instancia concreta de la entidad.

La fila de Ana es un usuario

La fila de Luis es otro usuario

No son “datos sueltos”, son objetos del mundo real representados de forma estructurada.

💡 Importante:

Todas las filas de una tabla siguen exactamente la misma estructura

No hay:

Campos opcionales arbitrarios

Estructuras cambiantes

Datos caóticos

Eso es intencional.

6. Clave primaria (Primary Key): la columna más importante

Toda tabla bien diseñada tiene una clave primaria (PK).

La clave primaria cumple tres reglas:

Identifica de forma única cada fila

No puede ser NULL

No puede repetirse

Ejemplo típico:

id → PRIMARY KEY


¿Por qué esto es tan crítico?

Porque:

Permite referenciar filas

Permite relaciones entre tablas

Evita duplicados ambiguos

Hace eficientes las búsquedas

👉 Sin clave primaria, una tabla es débil y peligrosa.

7. Relaciones: el corazón del modelo relacional

Aquí está la gran diferencia con otros sistemas.

Las tablas NO viven aisladas.
Se relacionan entre sí.

Ejemplo real:

Un usuario puede tener muchos pedidos

Un pedido pertenece a un usuario

Esto se modela con relaciones.

Ejemplo conceptual

Tabla usuarios:

id	nombre
1	Ana

Tabla pedidos:

id	usuario_id	total
10	1	50.00

Aquí:

usuarios.id → identifica al usuario

pedidos.usuario_id → referencia a ese usuario

Esto se llama clave foránea (Foreign Key).

8. Clave foránea: cómo se conectan las tablas

Una clave foránea (FK) es una columna que apunta a la clave primaria de otra tabla.

Regla fundamental:

pedidos.usuario_id → usuarios.id


Esto garantiza que:

No existan pedidos sin usuario

No existan referencias rotas

Los datos sean coherentes

👉 Esto se llama integridad referencial.

9. Tipos de relaciones (sin aún entrar en SQL)
1️⃣ Uno a uno (1:1)

Ejemplo:

Usuario ↔ Perfil

Cada usuario tiene un perfil, y cada perfil pertenece a un usuario.

2️⃣ Uno a muchos (1:N)

Ejemplo:

Usuario → Pedidos

Un usuario puede tener muchos pedidos.
Un pedido pertenece a un solo usuario.

👉 Es la relación más común.

3️⃣ Muchos a muchos (N:M)

Ejemplo:

Estudiantes ↔ Cursos

Un estudiante puede estar en varios cursos.
Un curso puede tener muchos estudiantes.

Esto se resuelve con una tabla intermedia, pero eso lo veremos más adelante.

10. Por qué las bases relacionales son tan estrictas

Puede parecer que ponen “demasiadas reglas”, pero esas reglas:

Previenen errores humanos

Evitan datos inconsistentes

Detectan bugs temprano

Protegen el sistema a largo plazo

💡 Regla de oro:

Cuanto más crítica es la información, más estricta debe ser la base de datos

Por eso:

Bancos → SQL

Pagos → SQL

Sistemas médicos → SQL

11. Diferencia clave con archivos (CSV / JSON)

Un CSV puede tener:

Columnas mal escritas

Tipos mezclados

Filas rotas

Una base relacional:

Impone estructura

Valida datos

Mantiene relaciones

Aplica reglas automáticamente

👉 SQL no confía en el programador.
Y eso es una virtud, no un defecto.

12. Error típico de principiantes (muy importante)

❌ “Primero guardo datos, luego pienso en relaciones”
❌ “Si algo falla lo arreglo en código”

Esto escala fatal.

La base de datos debe:

Defenderse sola

Impedir estados inválidos

Ser la última línea de defensa

13. Idea clave para cerrar este bloque

Una base de datos relacional no guarda datos.
Guarda relaciones entre hechos del mundo real.

Si entiendes esto, el resto de SQL empieza a tener sentido.