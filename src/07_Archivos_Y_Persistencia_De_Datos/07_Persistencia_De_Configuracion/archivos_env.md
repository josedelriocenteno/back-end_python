Archivos .env
Configuración, secretos y por qué esto NO es opcional
1. El problema fundamental que .env resuelve

Antes de hablar de .env, hay que entender el problema real.

Un programa necesita configuración:

credenciales

rutas

URLs

claves

flags

entornos (dev / prod)

Pregunta clave:

¿Dónde ponemos esos valores?

2. El error más peligroso que existe

Muchísima gente hace esto:

DB_PASSWORD = "supersecreta123"
API_KEY = "abc-xyz"


Esto es un error crítico.

Por qué:

Se sube a Git

Se filtra

Se copia

Se reutiliza

Se compromete seguridad

📌 Esto NO es un error teórico
Es uno de los fallos más comunes en producción real.

3. Qué es un archivo .env

Un archivo .env es:

Un archivo de texto

Que contiene variables de entorno

Que NO debe subirse a Git

Que separa configuración de código

Ejemplo:

DB_HOST=localhost
DB_PORT=5432
DB_USER=app_user
DB_PASSWORD=secreta
DEBUG=true

4. Qué son las variables de entorno (desde cero)

Una variable de entorno es:

Un par clave → valor

Gestionado por el sistema operativo

Accesible desde el programa

No viven en tu código
Viven en el entorno donde se ejecuta

5. Por qué separar configuración del código

Principio profesional:

El código no cambia entre entornos, la configuración sí

Ejemplo:

Entorno	DB_HOST
local	localhost
staging	staging-db
prod	prod-db

👉 El código es el mismo
👉 El .env cambia

6. Qué contiene un .env (y qué NO)
✔ Debe contener

Contraseñas

Tokens

URLs

Flags

Configuración dependiente del entorno

❌ NO debe contener

Lógica

Código

Datos grandes

Información pública

7. .env y Git: regla sagrada

El archivo .env NUNCA se sube al repositorio.

En su lugar:

.env → privado

.env.example → público

Ejemplo:

DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=


Esto documenta qué necesita el proyecto sin filtrar secretos.

8. Cómo se usa un .env en Python

Python no lee .env automáticamente.

Necesitas:

librería python-dotenv

Concepto clave:

.env → variables de entorno → os.environ

9. Flujo mental correcto
.env
 ↓
variables de entorno
 ↓
os.environ
 ↓
tu aplicación

10. Ejemplo mental (sin código todavía)

Supón:

DEBUG=true


Tu programa:

no sabe de .env

solo sabe que existe DEBUG en el entorno

📌 El .env solo inyecta valores

11. Por qué esto importa aún más en ML y Data

En ML tienes:

rutas de datasets

tamaños de batch

seeds

flags de entrenamiento

paths de modelos

Hardcodear esto:
❌ rompe reproducibilidad
❌ rompe entornos
❌ rompe pipelines

12. Error típico de juniors

“Es solo un proyecto pequeño”

Ese proyecto pequeño:

crece

se despliega

se comparte

Y ya es tarde.

13. Regla profesional definitiva

Si un valor cambia entre entornos → NO va en el código

14. Qué viene después

En el siguiente archivo ya entramos en código Python real para:

leer .env

validar configuración

usarla bien