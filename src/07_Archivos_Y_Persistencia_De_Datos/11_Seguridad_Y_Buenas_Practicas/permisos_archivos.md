permisos_archivos.md
Introducción

Los permisos de archivos determinan quién puede leer, modificar o ejecutar un archivo o directorio en un sistema operativo. Entenderlos es fundamental para:

Evitar errores de acceso en scripts Python.

Garantizar seguridad en proyectos y producción.

Evitar que datos sensibles sean modificados o leídos por usuarios no autorizados.

1️⃣ Conceptos básicos

Cada archivo o directorio tiene tres tipos de permisos:

Permiso	Descripción
r (read)	Permite leer el contenido del archivo o listar un directorio.
w (write)	Permite modificar o borrar el archivo.
x (execute)	Permite ejecutar un archivo como script o entrar en un directorio.

Y cada permiso se aplica a tres categorías de usuarios:

Owner → propietario del archivo.

Group → grupo al que pertenece el archivo.

Others → todos los demás usuarios.

Por ejemplo, en Linux:

-rwxr-xr--


rwx → Owner puede leer, escribir y ejecutar.

r-x → Group puede leer y ejecutar.

r-- → Others solo puede leer.

2️⃣ Ver permisos desde Python

Usando el módulo os:

import os

archivo = "datos.txt"

# Obtener permisos en formato octal
permisos = oct(os.stat(archivo).st_mode)[-3:]
print(f"Permisos actuales de {archivo}: {permisos}")


El valor octal representa los permisos: lectura=4, escritura=2, ejecución=1.

Por ejemplo, 644 significa:

Owner: 6 → 4+2 → leer + escribir

Group: 4 → leer

Others: 4 → leer

3️⃣ Cambiar permisos

Con os.chmod:

import os
import stat

archivo = "datos.txt"

# Dar permisos: solo owner puede leer y escribir, nadie más
os.chmod(archivo, stat.S_IRUSR | stat.S_IWUSR)

# Permisos completos para todos (no recomendable)
os.chmod(archivo, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)


stat.S_IRUSR → lectura para propietario

stat.S_IWUSR → escritura para propietario

stat.S_IXUSR → ejecución para propietario

Similar para G (grupo) y O (others).

4️⃣ Directorios y permisos

Para entrar en un directorio, se necesita el permiso x.

Para listar contenido, se necesita permiso r.

Para crear o borrar archivos, se necesita permiso w en el directorio.

Ejemplo:

import os

directorio = "proyecto"
os.chmod(directorio, stat.S_IRWXU)  # Owner puede leer, escribir, ejecutar

5️⃣ Buenas prácticas

Principio de mínimo privilegio: da solo los permisos necesarios.

Evitar 777: nunca des permisos completos a todos.

Archivos sensibles (contraseñas, tokens) → solo lectura para owner.

Logs → escritura controlada y rotación periódica.

Scripting seguro: siempre verifica que el script tenga acceso antes de operar sobre archivos críticos.

6️⃣ Ejemplo práctico

Supongamos que tienes un script que escribe resultados en resultados.txt:

import os
import stat

archivo = "resultados.txt"

# Crear archivo vacío
with open(archivo, "w") as f:
    f.write("Resultados de experimento\n")

# Dar permisos seguros: solo owner puede leer y escribir
os.chmod(archivo, stat.S_IRUSR | stat.S_IWUSR)

print(f"Archivo {archivo} creado con permisos seguros.")


Así, nadie más podrá leer ni modificar el archivo, evitando filtraciones accidentales.

7️⃣ Resumen

Permisos = control de lectura, escritura y ejecución.

Tres categorías: owner, group, others.

Usar os.stat para ver, os.chmod y stat para cambiar.

Aplicar mínimo privilegio para seguridad.

Considerar permisos también en directorios y pipelines automáticos.