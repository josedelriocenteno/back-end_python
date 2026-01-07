instalacion_postgresql.md
Instalación profesional de PostgreSQL (Local + Docker)
1. Antes de instalar nada: qué estás instalando exactamente

PostgreSQL no es una librería, es un servidor de base de datos.

Eso significa:

Es un proceso que corre en tu máquina

Escucha conexiones (puerto 5432 por defecto)

Gestiona memoria, disco, usuarios y permisos

Vive aunque tu programa Python no esté ejecutándose

👉 Esto es radicalmente distinto a “importar algo”.

2. Dos formas reales de usar PostgreSQL

En el mundo profesional hay dos escenarios principales:

PostgreSQL instalado directamente en tu sistema

PostgreSQL corriendo dentro de Docker

No son excluyentes. De hecho:

Aprenderás ambos

Usarás uno u otro según contexto

3. Opción A: PostgreSQL instalado en local (entender la base)
3.1 Cuándo usar instalación local

✔ Aprendizaje
✔ Desarrollo simple
✔ Entender cómo funciona el sistema
❌ No ideal para replicar producción compleja

3.2 Qué se instala realmente

Cuando instalas PostgreSQL en local, se instalan:

Servidor PostgreSQL

Cliente psql

Directorio de datos (data directory)

Usuario administrador (postgres)

3.3 Instalación en Linux (Ubuntu / Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib


Esto hace automáticamente:

Crea el usuario postgres

Inicia el servicio

Abre el puerto local

Comprobar estado:

sudo systemctl status postgresql

3.4 Acceder a PostgreSQL

Cambiar al usuario postgres:

sudo -i -u postgres


Entrar a la consola SQL:

psql


Si ves algo como:

postgres=#


✅ Estás dentro del motor de la base de datos.

3.5 Concepto clave: usuario del sistema vs usuario SQL

Esto es importante y muchos se lían aquí:

Usuario Linux: postgres

Usuario SQL: postgres

No son lo mismo, aunque compartan nombre.

👉 PostgreSQL tiene su propio sistema de usuarios.

4. Opción B: PostgreSQL con Docker (forma profesional)

Ahora vamos a lo realmente importante.

5. Qué es Docker (explicado sin humo)

Docker permite ejecutar software aislado, con:

Su propia configuración

Sus propios archivos

Su propio ciclo de vida

PostgreSQL en Docker significa:

No ensucia tu sistema

Se puede borrar y recrear

Es reproducible

Se parece a producción

6. Instalación de Docker (resumen)

Instala Docker Desktop o Docker Engine según tu sistema.

Comprueba:

docker --version


Si funciona, seguimos.

7. Levantar PostgreSQL con Docker (paso a paso)
7.1 Comando básico
docker run --name postgres-dev \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=app_db \
  -p 5432:5432 \
  -d postgres:16


Vamos línea por línea, sin asumir nada:

--name postgres-dev → nombre del contenedor

POSTGRES_PASSWORD → contraseña del usuario

POSTGRES_USER → usuario inicial

POSTGRES_DB → base de datos creada al inicio

-p 5432:5432 → expone el puerto

postgres:16 → versión exacta (muy importante)

👉 En producción nunca usas “latest”.

7.2 Verificar que está corriendo
docker ps


Debe aparecer postgres-dev.

7.3 Entrar a PostgreSQL dentro del contenedor
docker exec -it postgres-dev psql -U postgres -d app_db


Si ves:

app_db=#


🎯 Estás en una base de datos real, aislada y reproducible.

8. Persistencia en Docker (concepto crítico)

Si paras y borras el contenedor:

docker rm -f postgres-dev


👉 Pierdes los datos.

Para evitarlo se usan volúmenes:

docker run --name postgres-dev \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=app_db \
  -v postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres:16


Ahora:

Los datos viven fuera del contenedor

Puedes borrar el contenedor sin perder información

Esto es fundamental en producción.

9. Comparación clara: Local vs Docker
Aspecto	Local	Docker
Fácil de empezar	✅	⚠️
Reproducible	❌	✅
Aislado	❌	✅
Similar a prod	❌	✅
Limpio	❌	✅

👉 Conclusión profesional:

Aprende ambos

Usa Docker como estándar

10. Error típico de juniors

❌ Instalar PostgreSQL sin saber:

Qué usuario usa

Qué base de datos existe

Dónde viven los datos

❌ Usar “latest”

❌ No entender que es un servidor

11. Conexión mental importante (muy importante)

A partir de ahora:

PostgreSQL = sistema externo

Python = cliente

SQL = lenguaje de comunicación

Nada de esto es mágico.

12. Qué viene ahora (orden correcto)

Ya tienes:

Motor de base de datos

Acceso real

Entorno controlado

El siguiente paso lógico es: