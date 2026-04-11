# Inyección SQL: La Anatomía de un Desastre

La inyección SQL (SQLi) sigue siendo una de las vulnerabilidades más comunes y peligrosas del desarrollo web. Ocurre cuando un atacante logra "inyectar" código SQL malicioso a través de los campos de entrada de tu aplicación.

## 1. ¿Cómo funciona?

Imagina un código Python que construye una query así:
```python
# CÓDIGO VULNERABLE
query = "SELECT * FROM users WHERE email = '" + user_input + "'"
```

Si el atacante introduce esto en el campo email:
`' OR '1'='1`

La query resultante será:
`SELECT * FROM users WHERE email = '' OR '1'='1'`
**Resultado:** El atacante se loguea como el primer usuario de la base de datos (generalmente el admin) sin saber su contraseña.

## 2. El Ataque Destructivo

Si el atacante introduce:
`'; DROP TABLE users; --`

La query resultante será:
`SELECT * FROM users WHERE email = ''; DROP TABLE users; --'`
**Resultado:** Tu tabla de usuarios ha desaparecido. `--` comenta el resto de la query original para que no de error sintáctico.

## 3. La Única Defensa Real: Consultas Parametrizadas

Como vimos en el tema 08.08, el driver de la base de datos se encarga de que los inputs de usuario siempre sean tratados como **datos**, nunca como **código**.

```python
# CÓDIGO SEGURO
cur.execute("SELECT * FROM users WHERE email = %s", (user_input,))
```

## 4. Otros vectores de ataque (Blind SQLi)

A veces el atacante no recibe el resultado de la query, pero puede deducir información basándose en el **tiempo de respuesta**.
*   Inyecta un comando que hace que la DB espere 10 segundos si la primera letra de la contraseña del admin es 'A'.
*   Si la web tarda 10 segundos en cargar, el atacante ya sabe una letra. Repitiendo esto, puede extraer toda la base de datos.

## 5. Blindaje de Segundo Nivel

1.  **Principio de Menor Privilegio:** Como vimos en el tema anterior, si tu usuario de DB no tiene permiso para hacer `DROP TABLE`, el ataque anterior fallará.
2.  **Web Application Firewall (WAF):** Herramientas externas que detectan patrones de SQLi antes de que lleguen a tu código.
3.  **ORM:** Frameworks como Django o SQLAlchemy usan parámetros por defecto, protegiéndote del 90% de los ataques (¡pero cuidado con el uso de `text()` o `extra()`!).

## Resumen: Programe con Paranoia

1.  **Nunca confíes en el usuario.**
2.  **Nunca concatenes strings en un SQL.**
3.  **Usa siempre marcadores de posición (%s).**
4.  **Limita los permisos de tu base de datos.**
