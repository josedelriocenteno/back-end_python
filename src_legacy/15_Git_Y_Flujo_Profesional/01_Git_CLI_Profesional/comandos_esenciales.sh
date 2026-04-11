#!/bin/bash

# COMANDOS ESENCIALES PARA EL DÍA A DÍA
# -----------------------------------------------------------------------------

# 1. VER EL ESTADO
git status      # ¿Qué he cambiado?
git status -s   # Formato corto (limpio)

# 2. DIFERENCIAS
git diff               # Ver cambios que NO están en stage
git diff --staged      # Ver cambios que SÍ están en stage (listos para el commit)

# 3. HISTORIAL
git log                # Ver lista de commits
git log --oneline      # Un commit por línea
git log -p -2          # Ver los últimos 2 commits con sus diferencias (diff)

# 4. INSPECCIÓN
git show <hash>        # Ver qué cambió exactamente en ese commit
git show HEAD:archivo.py # Ver el contenido de un archivo en el último commit

# 5. GESTIÓN DE ARCHIVOS
git rm archivo.py      # Borra el archivo y lo añade al stage
git mv viejo.py nuevo.py # Renombra el archivo y lo añade al stage

# 6. LIMPIEZA
git clean -fd          # Borra todos los archivos que NO estén en Git (untracked)
                       # ¡Cuidado! Es irreversible.

# TIP SENIOR:
# Usa 'git diff --stat' para ver un resumen de cuántas líneas han cambiado
# en cada archivo sin ver todo el código. Ideal para revisiones rápidas.
