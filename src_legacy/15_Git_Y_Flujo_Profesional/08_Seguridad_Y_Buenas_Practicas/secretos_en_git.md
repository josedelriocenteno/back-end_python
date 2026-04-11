# Secretos en Git: Protegiendo tu infraestructura

Subir una clave de API, un password de base de datos o un token de AWS a Git es uno de los mayores riesgos de seguridad hoy en día. Si está en Git, está comprometido.

## 1. El error fatal: Commitear el `.env`
Una vez que subes un secreto a Git, aunque lo borres en el siguiente commit, **sigue en el historial**. Cualquiera puede viajar al pasado y leerlo.

## 2. Cómo limpiar un secreto ya subido
No basta con un commit nuevo. Debes reescribir la historia:
- Usa **trufflehog** o **gitleaks** para encontrar secretos olvidados en tu historial.
- Usa **BFG Repo-Cleaner** para eliminarlos de todos los commits de forma masiva.
- **IMPORTANTE:** Una vez subido el secreto, asume que está filtrado. **Cambia la clave inmediatamente** en el servicio correspondiente (AWS, Stripe, etc.).

## 3. Prevención con `.gitignore`
Asegúrate de que tu `.gitignore` incluye:
```text
.env
*.pem
secrets/
config.json (si contiene claves)
```

## 4. Gestión Profesional: Vaults y KMS
En lugar de archivos locales, los equipos senior usan:
- **GitHub Secrets:** Para variables de entorno en CI/CD.
- **HashiCorp Vault / AWS Secrets Manager:** La aplicación pide la clave al arrancar directamente al servicio de seguridad.

## 5. Herramientas de escaneo local (Pre-commit)
Configura un hook que escanee tu código **antes** de dejarte hacer commit en busca de patrones que parezcan una clave privada o un token de API.

## Resumen: La seguridad no es opcional
Tu repositorio debe poder ser público sin que eso suponga un riesgo para la empresa. Si necesitas una clave para que el código funcione, esa clave debe venir de fuera del repositorio.
