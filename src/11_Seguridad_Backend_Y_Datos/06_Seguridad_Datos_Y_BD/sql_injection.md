# SQL Injection: El Ataque que se Niega a Morir

La inyección SQL es una de las vulnerabilidades más antiguas, pero sigue apareciendo en reportes de seguridad año tras año. Ocurre cuando el backend confía ciegamente en lo que el usuario envía y lo concatena directamente en una consulta a la base de datos.

## 1. ¿Cómo funciona el ataque?
Imagina un código backend vulnerable:
```python
# CÓDIGO PELIGROSO - NO USAR
user_id = request.args.get('id')
query = f"SELECT * FROM users WHERE id = {user_id}"
db.execute(query)
```
Si el atacante envía como ID: `1; DROP TABLE users;`, la base de datos recibirá y ejecutará:
`SELECT * FROM users WHERE id = 1; DROP TABLE users;`
**Resultado:** Tus datos han sido borrados.

## 2. Tipos de SQL Injection
- **In-band (Classic):** El atacante ve el resultado del error o de la query directamente en la respuesta del navegador.
- **Inferential (Blind):** No se ve la respuesta, pero el atacante hace preguntas de tipo sí/no: "Si el primer carácter del password es una 'A', espera 5 segundos". Observando el tiempo de respuesta, puede reconstruir toda la base de datos.
- **Out-of-band:** El atacante logra que el servidor de DB haga una petición DNS o HTTP a un servidor controlado por él con los datos robados.

## 3. El mito de las "Escapadas de Caracteres"
Muchos desarrolladores piensan que usar `replace("'", "''")` es suficiente. Los atacantes senior tienen mil formas de saltarse estos filtros usando codificación UTF-8 rara, hexadecimales o manipulando otros campos que no parecen peligrosos.

## 4. Peligros más allá del SELECT
La inyección SQL no solo permite leer datos; puede:
- **Bypass de Login:** `admin' OR '1'='1` en el campo de usuario suele entrar como administrador.
- **Extracción de Archivos:** Usar comandos como `LOAD_FILE` de MySQL para leer archivos del servidor físico (ej: `/etc/passwd`).
- **Escalado a Shell:** En algunos sistemas (como MSSQL con `xp_cmdshell`), se puede llegar a ejecutar comandos del sistema operativo desde el SQL.

## Resumen: La cura es única y obligatoria
La única forma 100% segura de evitar la inyección SQL es **NUNCA concatenar variables** en la string de la consulta. Debes usar siempre **Consultas Parametrizadas** (Prepared Statements). No hay excusa válida para no hacerlo.
