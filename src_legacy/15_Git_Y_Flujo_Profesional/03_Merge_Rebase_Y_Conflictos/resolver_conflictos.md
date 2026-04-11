# Resolver Conflictos: Guía paso a paso

Los conflictos no son errores, son **puntos de decisión**. Ocurren cuando Git no sabe si quedarse con tu versión del código o con la versión del otro porque ambos habéis tocado la misma línea.

## 1. Identificar el Conflicto
Sabrás que hay un conflicto porque al hacer `merge` o `rebase` verás un mensaje:
`CONFLICT (content): Merge conflict in archivo.py`
`Automatic merge failed; fix conflicts and then commit the result.`

## 2. Anatomía de la Guerra
Git marca el archivo con estos símbolos:
```python
<<<<<<< HEAD
print("Esta es mi versión")
=======
print("Esta es la versión de mi compañero")
>>>>>>> branch-nombre
```

## 3. El Proceso de Resolución
1. **Analiza:** ¿Qué cambio es el correcto? ¿O quizás una mezcla de los dos?
2. **Limpia:** Borra los marcadores (`<<<`, `===`, `>>>`) y deja el archivo con el código final deseado.
3. **Marca como resuelto:** `git add archivo.py`.
4. **Finaliza:** `git commit` (en caso de merge) o `git rebase --continue` (en caso de rebase).

## 4. Herramientas de Ayuda
No uses Word o editores de texto plano. Usa:
- **VS Code Editor de Conflictos:** Te da botones para "Accept Current", "Accept Incoming" y una vista dividida muy útil.
- **git mergetool:** Si configuras herramientas como Meld o KDiff3.

## 5. REGLA DE ORO: No borres a ciegas
Muchos desarrolladores borran el código del compañero por las prisas. Antes de decidir qué borrar, si no estás seguro, **pregunta** a la persona que escribió la otra versión.

## Resumen: Mantén la Calma
Un conflicto es Git pidiéndote ayuda. Tómate tu tiempo, lee el código de ambas partes y asegúrate de que, tras la resolución, la aplicación sigue pasando los tests.
