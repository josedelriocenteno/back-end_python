"""
SEGURIDAD: PASSWORD HASHING PROFESIONAL
-----------------------------------------------------------------------------
NUNCA guardes contraseñas en texto plano. En su lugar, guarda un 'hash'.
Un hash es una representación unidireccional de los datos (irreversible).
"""

from passlib.context import CryptContext

# 1. EL CONTEXTO DE CIFRADO
# Usamos Bcrypt por defecto, que es el estándar de la industria.
# Es un algoritmo 'lento' diseñado para ser resistente a la fuerza bruta.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Convierte una contraseña plana en un hash seguro con 'Salt' automático.
    El 'Salt' es un dato aleatorio extra que se añade para evitar que 
    dos contraseñas iguales tengan el mismo hash.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Comprueba si la contraseña plana coincide con el hash guardado.
    """
    return pwd_context.verify(plain_password, hashed_password)

# --- EJEMPLO DE USO ---
password_usuario = "mi_secreto_123"

# En el momento del registro:
password_segura = hash_password(password_usuario)
print(f"Password original: {password_usuario}")
print(f"Hash guardado en DB (60 caracteres): {password_segura}")

# En el momento del login:
login_intent = "mi_secreto_123"
es_valida = verify_password(login_intent, password_segura)

if es_valida:
    print("✅ Login exitoso")
else:
    print("❌ Contraseña incorrecta")

"""
DIFERENCIA ENTRE HASHEAR Y CIFRAR (IMPORTANTE):
-----------------------------------------------------------------------------
1. CIFRAR (Encryption): Es reversible. Tienes una llave para cifrar y otra 
   para descifrar. Se usa para datos que TÚ necesitas leer después (ej: SSN).
2. HASHEAR (Hashing): Es IRREVERSIBLE. No hay una llave para "des-hashear". 
   Se usa para contraseñas porque el servidor nunca necesita saber tu 
   contraseña real, solo si la que envías coincide con lo que guardamos.
"""

"""
ALGORITMOS MODERNOS RECOMENDADOS:
- Bcrypt: El más compatible y probado.
- Argon2id: El ganador del concurso de hashing, extremadamente robusto contra 
  ataques con GPUs potentes.
- Scrypt: Diseñado para requerir mucha memoria.
"""
