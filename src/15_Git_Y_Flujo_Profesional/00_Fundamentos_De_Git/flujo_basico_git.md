# Flujo Básico: add → commit → push

Este es el latido del corazón del desarrollador. Es la secuencia de comandos que repetirás miles de veces a lo largo de tu carrera.

## 1. Preparar el terreno (`git add`)
"Poner los archivos en la maleta antes de viajar".
```bash
git add main.py          # Añade un archivo específico
git add .                # Añade TODOS los cambios de la carpeta actual
git add -p               # Elige qué partes de un archivo añadir (Modo Pro)
```

## 2. Consolidar el cambio (`git commit`)
"Cerrar la maleta y ponerle una etiqueta con la fecha y el contenido".
```bash
git commit -m "feat: añadido endpoint de usuarios"
```
Un commit debe ser **Atómico**: resolver una sola cosa. Si arreglas un bug y añades una función, haz dos commits.

## 3. Compartir con el mundo (`git push`)
"Subir la maleta al avión hacia el almacén central (GitHub)".
```bash
git push origin main
```

## 4. Traer cambios de otros (`git pull`)
"Descargar las maletas nuevas que otros han enviado al almacén".
```bash
git pull origin main
```

## 5. El ciclo de vida de un archivo
1. **Untracked:** Git no sabe que existe.
2. **Unmodified:** Ya está en Git y no ha cambiado.
3. **Modified:** Ha cambiado pero no está en la maleta.
4. **Staged:** Está en la maleta listo para el commit.

## Resumen: Sin miedo al terminal
Este flujo asegura que tu trabajo esté respaldado y sincronizado. La regla de oro es: **Commitea a menudo, Pullea siempre antes de empezar y Pushea cuando hayas terminado una unidad de trabajo.**
