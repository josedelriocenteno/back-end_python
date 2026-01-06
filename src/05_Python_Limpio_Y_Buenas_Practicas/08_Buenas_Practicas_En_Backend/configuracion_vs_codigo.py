"""
configuracion_vs_codigo.py
==========================

Buenas prácticas: separar configuración de código

Objetivos:
- Evitar “hardcode” de configuraciones
- Usar variables de entorno y archivos de settings
- Facilitar despliegue, testeo y mantenimiento
- Aumentar seguridad y portabilidad
"""

# -------------------------------------------------------------------
# 1️⃣ PROBLEMA: CONFIGURACIÓN DENTRO DEL CÓDIGO
# -------------------------------------------------------------------

# ❌ MAL: valores "hardcodeados"
class ServicioEmailMagico:
    def enviar(self, destinatario: str, mensaje: str):
        smtp_host = "smtp.gmail.com"  # hardcodeado
        smtp_port = 587  # hardcodeado
        usuario = "admin@gmail.com"
        password = "contraseña-secreta"  # inseguro
        print(f"Enviando email a {destinatario} usando {smtp_host}:{smtp_port}")

# Problemas:
# 1. Difícil cambiar host, puerto, credenciales según entorno
# 2. No seguro: secretos expuestos
# 3. Difícil de testear en entornos distintos


# -------------------------------------------------------------------
# 2️⃣ SOLUCIÓN: CONFIGURACIÓN EXTERNA (ENV / SETTINGS)
# -------------------------------------------------------------------

# Usando variables de entorno y módulo de configuración
import os
from dataclasses import dataclass

# Archivo: settings.py
@dataclass
class EmailSettings:
    smtp_host: str
    smtp_port: int
    usuario: str
    password: str

# Función para cargar configuración desde variables de entorno
def cargar_email_settings() -> EmailSettings:
    return EmailSettings(
        smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.getenv("SMTP_PORT", 587)),
        usuario=os.getenv("SMTP_USER", "admin@gmail.com"),
        password=os.getenv("SMTP_PASS", "default-password")
    )

# Servicio de email usando configuración externa
class ServicioEmail:
    def __init__(self, config: EmailSettings):
        self._config = config

    def enviar(self, destinatario: str, mensaje: str):
        print(f"Enviando email a {destinatario} usando {self._config.smtp_host}:{self._config.smtp_port}")
        # Aquí iría la lógica real de envío usando self._config.usuario / password


# -------------------------------------------------------------------
# 3️⃣ USO EN DISTINTOS ENTORNOS
# -------------------------------------------------------------------

# 1. Entorno de desarrollo
os.environ["SMTP_USER"] = "dev@gmail.com"
os.environ["SMTP_PASS"] = "dev-pass"

config_dev = cargar_email_settings()
servicio_dev = ServicioEmail(config_dev)
servicio_dev.enviar("usuario@dev.com", "Hola Dev!")

# 2. Entorno de producción
os.environ["SMTP_USER"] = "prod@gmail.com"
os.environ["SMTP_PASS"] = "prod-pass"

config_prod = cargar_email_settings()
servicio_prod = ServicioEmail(config_prod)
servicio_prod.enviar("usuario@prod.com", "Hola Prod!")


# -------------------------------------------------------------------
# 4️⃣ BENEFICIOS
# -------------------------------------------------------------------

# 1. Separación clara entre código y configuración
# 2. Facilita despliegue en distintos entornos (dev, staging, prod)
# 3. Mejora seguridad: secretos no hardcodeados
# 4. Facilita testeo con mocks o variables de entorno distintas
# 5. Código más limpio y mantenible


# -------------------------------------------------------------------
# 5️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Separar configuración = código profesional
# Principios clave:
# - Nunca hardcodees valores de configuración (URLs, credenciales, rutas)
# - Usa variables de entorno o archivos de settings
# - Permite flexibilidad y seguridad en entornos múltiples
# - Mantén código limpio y portable
