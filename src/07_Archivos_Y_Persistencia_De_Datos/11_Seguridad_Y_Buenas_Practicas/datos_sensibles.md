datos_sensibles.md
Introducción

En cualquier proyecto de software o Data/ML, algunas piezas de información son críticas y sensibles, como:

Contraseñas y tokens de APIs.

Credenciales de bases de datos.

Información personal de usuarios (emails, nombres, números de identificación, etc.).

Claves privadas y secretos criptográficos.

Guardar estos datos en texto plano o en código fuente es un riesgo enorme:

Si el repositorio se publica accidentalmente → filtración inmediata.

Alguien con acceso al servidor puede robar información.

Es difícil rotar o cambiar secretos si están dispersos en archivos de código.

Objetivo: manejar estos datos de forma segura, reproducible y práctica en Python.

1️⃣ Nunca en texto plano en código

Mal ejemplo:

# INCORRECTO
DB_PASSWORD = "miSuperSecreta123"


Problemas:

Cualquier persona con acceso al código ve la contraseña.

Difícil de cambiar si se despliega a producción.

Repositorios públicos → exposición directa.

2️⃣ Variables de entorno (.env)

Una práctica estándar es guardar datos sensibles en variables de entorno:

Crear un archivo .env:

DB_USER=usuario
DB_PASSWORD=miSuperSecreta123
API_KEY=abc123xyz


Leer estas variables en Python con python-dotenv:

from dotenv import load_dotenv
import os

# Cargar archivo .env
load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
api_key = os.getenv("API_KEY")

print(f"Usuario DB: {db_user}")
# No imprimir nunca el password en logs


Buenas prácticas con .env:

Nunca subir .env al repositorio.

Crear un .env.example con nombres de variables, pero sin valores reales.

Usar diferentes .env para desarrollo, testing y producción.

3️⃣ Archivos de configuración seguros

A veces necesitas almacenar secretos en archivos de configuración:

INI, JSON o YAML.

Cifrar los archivos para que no se puedan leer en texto plano.

Ejemplo simple con cryptography:

from cryptography.fernet import Fernet

# Generar clave secreta (solo una vez)
clave = Fernet.generate_key()
fernet = Fernet(clave)

# Guardar secreto cifrado
secreto = "miSuperSecreto"
secreto_cifrado = fernet.encrypt(secreto.encode())

# Guardar en archivo
with open("secret.enc", "wb") as f:
    f.write(secreto_cifrado)

# Leer y descifrar
with open("secret.enc", "rb") as f:
    contenido = f.read()
secreto_descifrado = fernet.decrypt(contenido).decode()
print(secreto_descifrado)  # miSuperSecreto


Nota: La clave clave debe almacenarse de forma segura, idealmente en un vault seguro.

4️⃣ Gestores de secretos (vaults)

Para proyectos serios:

AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault.

Permiten:

Guardar y rotar secretos de forma segura.

Integración con código sin exponer valores en texto plano.

Auditar accesos y mantener control centralizado.

Ejemplo (pseudocódigo AWS boto3):

import boto3

client = boto3.client("secretsmanager")
response = client.get_secret_value(SecretId="miDBPassword")
db_password = response["SecretString"]

5️⃣ Evitar logs y prints de secretos

Nunca hagas print(db_password) en desarrollo.

Logs en producción deben ocultar valores sensibles.

Si un valor debe aparecer en logs, usa máscaras:

print(f"API_KEY = {api_key[:4]}****")

6️⃣ Encriptación de datos sensibles

Si necesitas guardar información confidencial en base de datos:

Usa hashing para contraseñas (bcrypt, argon2).

Usa AES o RSA para cifrar datos que deban recuperarse.

Nunca almacenar contraseñas en texto plano.

Ejemplo hashing con bcrypt:

import bcrypt

password = b"miPasswordSecreto"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# Verificar
if bcrypt.checkpw(password, hashed):
    print("Contraseña correcta")

7️⃣ Buenas prácticas resumen

Nunca guardar secretos en texto plano.

Variables de entorno para secretos de configuración.

Archivos cifrados si es necesario almacenar localmente.

Vaults y gestores de secretos para producción.

No loguear datos sensibles, usa masking si es necesario.

Hashear contraseñas y cifrar datos críticos.

Versionado seguro: .env no va en repositorio; solo un .env.example.

Con esto, tu código estará mucho más seguro, mantenible y profesional, evitando fugas de información y cumpliendo buenas prácticas de seguridad.