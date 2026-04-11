# Ramas en Git: ¿Qué son realmente?

Olvídate de carpetas paralelas. Una rama en Git es algo mucho más ligero y potente.

## 1. El Puntero Movible
Técnicamente, una rama es simplemente un **puntero móvil** a uno de tus commits. Cuando haces un commit, el puntero de la rama actual se mueve automáticamente hacia adelante.

## 2. La rama `main` (o `master`)
Es la rama por defecto. En producción, suele representar el código estable que el usuario final está usando.

## 3. Crear y cambiar de rama
```bash
git branch nueva-funcionalidad    # Crea la rama
git checkout nueva-funcionalidad  # Se mueve a ella
# O en un solo comando (Moderno):
git switch -c nueva-funcionalidad
```

## 4. Por qué usamos ramas
- **Aislamiento:** Puedes romper el código en una rama sin que la versión estable se vea afectada.
- **Paralelismo:** Varios desarrolladores pueden trabajar en funciones diferentes al mismo tiempo.
- **Experimentación:** Crea una rama para probar una idea loca; si no funciona, simplemente la borras.

## 5. Listar e inspeccionar
- `git branch`: Lista las ramas locales.
- `git branch -a`: Lista locales y remotas.
- `git branch -v`: Muestra el último commit de cada rama.

## Resumen: Ramas Baratas
En otros sistemas de control de versiones, crear una rama implicaba copiar todos los archivos físicos. En Git, crear una rama es crear un archivo de 41 bytes que guarda el hash de un commit. Úsalas sin miedo; son baratas, rápidas y fundamentales.
