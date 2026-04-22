# ===========================================================================
# 04_strings_completo.py
# ===========================================================================
# MÓDULO 01: FUNDAMENTOS Y TIPOS
# ARCHIVO 04: Strings — El tipo de dato más usado en programación
# ===========================================================================
#
# OBJETIVO DE ESTE ARCHIVO:
# Dominar strings en Python desde cero absoluto hasta nivel profesional.
# Incluye encoding (UTF-8/Unicode), f-strings avanzados, todos los métodos,
# slicing, inmutabilidad, y la conexión directa con NLP/procesamiento de
# texto, que es LA aplicación más importante de strings para un Ingeniero IA.
#
# NIVEL: Desde cero con profundidad extrema.
# ===========================================================================


# ===========================================================================
# CAPÍTULO 1: ¿QUÉ ES UN STRING?
# ===========================================================================

"""
Un string (cadena de texto) es una SECUENCIA INMUTABLE de caracteres.

"Secuencia" = tiene orden, puedes acceder por posición (índice)
"Inmutable" = una vez creado, NO puedes modificar sus caracteres
"Caracteres" = letras, números, espacios, emojis, cualquier símbolo Unicode

En Python, el tipo se llama 'str'.
NO hay un tipo 'char' separado (como en C o Java).
Un carácter es simplemente un string de longitud 1.
"""

# Formas de crear strings:
print("=== CREACIÓN DE STRINGS ===")

# Comillas simples y dobles son EQUIVALENTES
s1 = 'hola'
s2 = "hola"
print(f"'hola' == \"hola\": {s1 == s2}")  # True

# ¿Cuándo usar simples vs dobles?
# → Usa la que te evite escapar comillas internas:
dialogo = "Él dijo: 'esto funciona'"         # comillas dobles fuera
html = '<div class="container">texto</div>'  # comillas simples fuera
print(dialogo)
print(html)

# Comillas triples: strings multilínea
poema = """Esto es un string
que ocupa varias líneas.
Cada salto de línea se preserva."""
print(f"\nString multilínea:\n{poema}")

# También sirven para docstrings (documentación de funciones/clases)
def mi_funcion():
    """Esta es la documentación de la función.
    
    Puede ser multilínea y usa triple comillas.
    """
    pass

print(f"\nDocstring de mi_funcion: {mi_funcion.__doc__}")

# String vacío
vacio = ""
print(f"\nString vacío: '{vacio}', len = {len(vacio)}, bool = {bool(vacio)}")

# String de un solo carácter (no existe tipo char en Python)
letra = "A"
print(f"type('A') = {type(letra)}")  # str, no char


# ===========================================================================
# CAPÍTULO 2: UNICODE Y ENCODING — CÓMO SE ALMACENA EL TEXTO
# ===========================================================================

"""
ESTO ES FUNDAMENTAL PARA NLP Y PROCESAMIENTO DE TEXTO.

HISTORIA BREVE:
===============
1. ASCII (1963): 128 caracteres. Solo inglés.
   'A' = 65, 'a' = 97, '0' = 48

2. Latin-1/ISO-8859-1: 256 caracteres. Inglés + acentos europeos.
   Pero no cubre chino, japonés, árabe, emoji...

3. Unicode (1991): UN ESTÁNDAR que asigna un número único a CADA
   carácter de TODOS los idiomas del mundo + emojis + símbolos.
   Actualmente hay ~150,000 caracteres definidos.

   'A' = U+0041
   'ñ' = U+00F1
   '€' = U+20AC
   '你' = U+4F60  (chino: "tú")
   '🔥' = U+1F525

   Cada carácter tiene un "code point" (número único).

4. UTF-8 (1993): Una CODIFICACIÓN (encoding) que traduce code points
   Unicode a bytes para almacenamiento.
   
   - Caracteres ASCII (0-127): 1 byte
   - Caracteres europeos acentuados: 2 bytes
   - Caracteres CJK (chino, japonés, coreano): 3 bytes
   - Emojis: 4 bytes

   UTF-8 es el encoding ESTÁNDAR de internet y de Python 3.

EN PYTHON 3:
  - Los strings (str) son secuencias de caracteres Unicode
  - Los archivos .py se leen como UTF-8 por defecto
  - Puedes usar cualquier carácter Unicode en tu código
"""

print("\n=== UNICODE Y ENCODING ===")

# Caracteres Unicode en strings
texto_es = "español: ñ, á, é, ü"
texto_cn = "中文: 你好世界"
texto_ar = "العربية: مرحبا"
texto_em = "emojis: 🔥🤖🧠"

for texto in [texto_es, texto_cn, texto_ar, texto_em]:
    print(f"  '{texto}' → len={len(texto)}")

# ATENCIÓN: len() cuenta CARACTERES, no bytes
emoji = "🔥"
print(f"\n'🔥' tiene {len(emoji)} carácter(es)")
print(f"'🔥' ocupa {len(emoji.encode('utf-8'))} bytes en UTF-8")

# ord() → carácter a code point
# chr() → code point a carácter
print(f"\nord('A') = {ord('A')}")          # 65
print(f"ord('ñ') = {ord('ñ')}")          # 241
print(f"ord('🔥') = {ord('🔥')}")        # 128293
print(f"chr(65) = '{chr(65)}'")           # 'A'
print(f"chr(241) = '{chr(241)}'")         # 'ñ'
print(f"chr(128293) = '{chr(128293)}'")   # '🔥'

# Encoding y decoding
texto = "Hola, 世界! 🌍"
bytes_utf8 = texto.encode('utf-8')    # str → bytes
print(f"\nOriginal: '{texto}'")
print(f"Encoded (UTF-8): {bytes_utf8}")
print(f"Tipo: {type(bytes_utf8)}")
print(f"Decoded: '{bytes_utf8.decode('utf-8')}'")

"""
¿POR QUÉ IMPORTA PARA IA / NLP?
=================================
1. TOKENIZACIÓN: Los LLMs no procesan texto directamente. Lo tokenizan.
   Un tokenizador divide texto en "tokens" (subpalabras, caracteres, bytes).
   Entender Unicode es esencial para entender tokenización.

2. MULTILINGÜE: Si entrenas un modelo que habla español, chino e inglés,
   necesitas entender cómo se codifican estos idiomas.

3. LIMPIEZA DE DATOS: El 80% del trabajo de NLP es limpiar texto sucio.
   Caracteres raros, BOM markers, encoding incorrecto, mojibake...

4. EMBEDDINGS: Cada token se convierte en un vector numérico (embedding).
   La calidad del tokenizador afecta directamente al rendimiento del modelo.

5. COSTES DE API: Los LLMs cobran por TOKEN. Un emoji puede costar
   más tokens que una palabra entera. Entender esto es entender costes.
"""


# ===========================================================================
# CAPÍTULO 3: SECUENCIAS DE ESCAPE
# ===========================================================================

print("\n=== SECUENCIAS DE ESCAPE ===")

# Las secuencias de escape comienzan con \
print("Salto de línea: línea1\\nlínea2")
print("Línea 1\nLínea 2")          # \n = nueva línea
print("Tabulación:\taquí")          # \t = tabulación
print("Barra invertida: \\")       # \\ = \
print("Comilla simple: \'")        # \' = '
print("Comilla doble: \"")         # \" = "
print("Retorno carro: hola\rmundo")  # \r = retorno de carro

# Caracteres Unicode por code point
print(f"\\u00f1 = '\u00f1'")       # ñ (4 dígitos hex)
print(f"\\U0001F525 = '\U0001F525'") # 🔥 (8 dígitos hex)
print(f"\\N{{FIRE}} = '\N{FIRE}'")    # 🔥 (por nombre Unicode)

# RAW STRINGS: ignoran secuencias de escape
raw = r"C:\Users\nombre\archivo.txt"
print(f"\nRaw string: {raw}")  # Los \n \a no se interpretan

"""
Los raw strings (r"...") son ESENCIALES para:
  - Rutas de archivo en Windows
  - Expresiones regulares (regex)
  - Cualquier texto que contenga \ literal

En NLP, usar raw strings para regex es obligatorio:
  import re
  patron = r"\b\w+\b"  # sin r, \b sería un backspace
"""


# ===========================================================================
# CAPÍTULO 4: INDEXACIÓN Y SLICING — ACCESO A CARACTERES
# ===========================================================================

"""
Los strings son SECUENCIAS, así que puedes acceder a caracteres
individuales y extraer substrings.

INDEXACIÓN:
  s[i]  → carácter en posición i

  Índices positivos: 0, 1, 2, ... (desde el inicio)
  Índices negativos: -1, -2, ... (desde el final)

  "python"
   p  y  t  h  o  n
   0  1  2  3  4  5    (positivos)
  -6 -5 -4 -3 -2 -1    (negativos)
"""

print("\n=== INDEXACIÓN ===")

s = "python"
print(f"s = '{s}'")
print(f"s[0]  = '{s[0]}'")    # 'p' — primer carácter
print(f"s[1]  = '{s[1]}'")    # 'y'
print(f"s[-1] = '{s[-1]}'")   # 'n' — último carácter
print(f"s[-2] = '{s[-2]}'")   # 'o'

# Error si el índice NO existe:
try:
    print(s[10])
except IndexError as e:
    print(f"Error: {e}")  # string index out of range

"""
SLICING (rebanado):
  s[inicio:fin]        → desde inicio HASTA fin (sin incluir fin)
  s[inicio:fin:paso]   → con un paso

  Si omites inicio → desde el principio (0)
  Si omites fin → hasta el final (len(s))
  Si omites paso → paso de 1
"""

print("\n=== SLICING ===")

s = "inteligencia artificial"
print(f"s = '{s}'")
print(f"s[0:12]   = '{s[0:12]}'")     # 'inteligencia'
print(f"s[13:]    = '{s[13:]}'")       # 'artificial'
print(f"s[:12]    = '{s[:12]}'")       # 'inteligencia' (desde inicio)
print(f"s[-10:]   = '{s[-10:]}'")      # 'artificial' (últimos 10)
print(f"s[::2]    = '{s[::2]}'")       # 'itlgni riicl' (cada 2)
print(f"s[::-1]   = '{s[::-1]}'")      # string invertido

# Slicing NUNCA da error por índices fuera de rango:
print(f"s[0:1000] = '{s[0:1000]}'")    # devuelve todo, sin error
print(f"s[100:200]= '{s[100:200]}'")   # string vacío, sin error

"""
SLICING EN IA:
  - Truncar secuencias a longitud máxima: texto[:max_tokens]
  - Obtener prefijos/sufijos para augmentación de datos
  - Procesar texto en ventanas: texto[i:i+window_size]
  - Invertir secuencias es raro pero aparece en algunos modelos
"""


# ===========================================================================
# CAPÍTULO 5: INMUTABILIDAD DE STRINGS
# ===========================================================================

print("\n=== INMUTABILIDAD ===")

s = "hola"
# NO puedes modificar un carácter:
try:
    s[0] = "H"
except TypeError as e:
    print(f"Error: {e}")

# Para "modificar", creas un string NUEVO:
s_nuevo = "H" + s[1:]
print(f"Original: '{s}', Nuevo: '{s_nuevo}'")

# Esto crea un nuevo objeto:
s = "hola"
id_antes = id(s)
s = s + " mundo"
id_despues = id(s)
print(f"\nid antes:   {id_antes}")
print(f"id después: {id_despues}")
print(f"Mismo objeto: {id_antes == id_despues}")  # False

"""
IMPLICACIÓN DE RENDIMIENTO:
Si concatenas strings en un bucle, es MUY ineficiente:

  # ❌ MAL — O(n²): crea un nuevo string en cada iteración
  resultado = ""
  for palabra in lista_palabras:
      resultado += palabra + " "

  # ✅ BIEN — O(n): une todo al final
  resultado = " ".join(lista_palabras)

¿Por qué? Cada += crea un string nuevo, copia todo el contenido
anterior más el nuevo texto. Si tienes 10,000 palabras, la última
iteración copia 9,999 palabras solo para añadir 1.

join() genera el string final en una sola operación.

Esto es CRÍTICO en NLP cuando procesas miles de documentos.
"""

# Demostración de rendimiento:
import time

palabras = ["token"] * 50000

# Método lento (concatenación)
start = time.perf_counter()
resultado = ""
for p in palabras:
    resultado += p + " "
tiempo_concat = time.perf_counter() - start

# Método rápido (join)
start = time.perf_counter()
resultado = " ".join(palabras)
tiempo_join = time.perf_counter() - start

print(f"\nConcatenación: {tiempo_concat:.4f}s")
print(f"join():        {tiempo_join:.6f}s")
print(f"join() es ~{tiempo_concat/tiempo_join:.0f}x más rápido")


# ===========================================================================
# CAPÍTULO 6: MÉTODOS DE STRING — REFERENCIA COMPLETA
# ===========================================================================

"""
Los strings tienen MUCHOS métodos built-in. Aquí van TODOS los
importantes, con ejemplos y cuándo los usarás en la práctica.

REGLA: Todos los métodos devuelven un string NUEVO (no modifican el original,
porque los strings son inmutables).
"""

print("\n" + "=" * 60)
print("=== MÉTODOS DE STRING — REFERENCIA COMPLETA ===")
print("=" * 60)

# ─── BÚSQUEDA Y COMPROBACIÓN ───
print("\n--- Búsqueda y comprobación ---")

texto = "  Machine Learning con Python 3.12  "

# .find(sub) → posición de la primera ocurrencia, -1 si no está
print(f"'Learning'.find en '{texto.strip()}': {texto.find('Learning')}")
print(f"'Java'.find: {texto.find('Java')}")  # -1

# .index(sub) → como find, pero lanza ValueError si no está
try:
    texto.index("Java")
except ValueError as e:
    print(f".index('Java'): ValueError — {e}")

# .count(sub) → cuántas veces aparece
s = "abracadabra"
print(f"'a' aparece {s.count('a')} veces en '{s}'")

# .startswith() / .endswith()
archivo = "modelo_v2.pt"
print(f"'{archivo}'.endswith('.pt'): {archivo.endswith('.pt')}")
print(f"'{archivo}'.startswith('modelo'): {archivo.startswith('modelo')}")
# Aceptan tuplas:
print(f"'.pt' o '.pth': {archivo.endswith(('.pt', '.pth'))}")

# in → comprobación de contenido (operador, no método)
print(f"'Python' in texto: {'Python' in texto}")

"""
EN NLP/IA:
  - endswith() para filtrar archivos: [f for f in files if f.endswith('.csv')]
  - startswith() para detectar prefijos en tokens
  - count() para frecuencia de caracteres/substrings
  - 'in' para búsqueda rápida de patrones
"""

# ─── TRANSFORMACIÓN DE CASO ───
print("\n--- Transformación de caso ---")

s = "hOlA MuNdO de LA ia"

print(f"upper():    '{s.upper()}'")       # 'HOLA MUNDO DE LA IA'
print(f"lower():    '{s.lower()}'")       # 'hola mundo de la ia'
print(f"title():    '{s.title()}'")       # 'Hola Mundo De La Ia'
print(f"capitalize(): '{s.capitalize()}'")# 'Hola mundo de la ia'
print(f"swapcase(): '{s.swapcase()}'")    # 'HoLa mUnDo DE la IA'
print(f"casefold(): '{s.casefold()}'")    # como lower() pero más agresivo (Unicode)

"""
casefold() vs lower():
  "STRASSE".lower() → "strasse"
  "STRAßE".lower() → "straße"      ← ß no cambia con lower()
  "STRAßE".casefold() → "strasse"  ← casefold() convierte ß a ss

Para NLP SIEMPRE usa casefold() en vez de lower() si trabajas con
texto multilingüe. Es más robusto para normalización.
"""

# ─── LIMPIEZA Y ESPACIOS ───
print("\n--- Limpieza y espacios ---")

sucio = "  \t  Machine Learning  \n  "
print(f"strip():  '{sucio.strip()}'")      # quita espacios/tabulaciones/newlines
print(f"lstrip(): '{sucio.lstrip()}'")     # solo izquierda
print(f"rstrip(): '{sucio.rstrip()}'")     # solo derecha

# strip con caracteres específicos:
url = "///path/to/file///"
print(f"strip('/'): '{url.strip('/')}'")   # 'path/to/file'

# Reemplazo
texto = "Python es lento, Python es fácil"
print(f"\nreplace: '{texto.replace('Python', 'Rust')}'")  # Reemplaza TODOS
print(f"replace(1): '{texto.replace('Python', 'Rust', 1)}'")  # Solo el primero

"""
EN NLP:
  strip() es FUNDAMENTAL para limpiar texto:
  - Quitar espacios al inicio/final
  - Quitar caracteres BOM (\ufeff)
  - Limpiar newlines de archivos

  replace() para normalización:
  - Reemplazar comillas tipográficas por normales
  - Normalizar espacios múltiples
  - Quitar caracteres no deseados
"""

# ─── DIVISIÓN Y UNIÓN ───
print("\n--- División y unión ---")

# .split() — divide string en lista
csv_line = "nombre,edad,ciudad,profesión"
partes = csv_line.split(",")
print(f"split(','): {partes}")

# split sin argumento → divide por cualquier espacio
texto = "hola    mundo\t\tjusto\n\nahora"
print(f"split(): {texto.split()}")  # ['hola', 'mundo', 'justo', 'ahora']

# splitlines() — divide por saltos de línea
multilinea = "línea 1\nlínea 2\nlínea 3"
print(f"splitlines(): {multilinea.splitlines()}")

# Limitar divisiones
datos = "a:b:c:d:e"
print(f"split(':', 2): {datos.split(':', 2)}")  # ['a', 'b', 'c:d:e']

# .join() — une una lista en un string
palabras = ["Machine", "Learning", "Engineer"]
print(f"' '.join(): '{' '.join(palabras)}'")
print(f"', '.join(): '{', '.join(palabras)}'")
print(f"'→'.join(): '{'→'.join(palabras)}'")

"""
split() + join() es el DÚO MÁS USADO en procesamiento de texto:

  # Normalizar espacios:
  " ".join(texto.split())

  # Tokenización básica (naive):
  tokens = texto.lower().split()

  # CSV parsing (básico):
  campos = linea.split(",")

  # Reconstruir texto:
  texto_limpio = " ".join(tokens_filtrados)
"""

# ─── VALIDACIÓN DE CONTENIDO ───
print("\n--- Validación de contenido ---")

print(f"'42'.isdigit():    {'42'.isdigit()}")        # True
print(f"'3.14'.isdigit():  {'3.14'.isdigit()}")      # False (tiene .)
print(f"'abc'.isalpha():   {'abc'.isalpha()}")        # True
print(f"'abc123'.isalnum():{'abc123'.isalnum()}")     # True (alfanumérico)
print(f"'  '.isspace():    {'  '.isspace()}")         # True
print(f"'ABC'.isupper():   {'ABC'.isupper()}")        # True
print(f"'abc'.islower():   {'abc'.islower()}")        # True
print(f"'Hello'.istitle():  {'Hello World'.istitle()}")  # True
print(f"'var_name'.isidentifier(): {'var_name'.isidentifier()}")  # True
print(f"'42var'.isidentifier(): {'42var'.isidentifier()}")  # False

# ─── ALINEACIÓN Y PADDING ───
print("\n--- Alineación y padding ---")

titulo = "IA"
print(f"center(20, '-'): '{titulo.center(20, '-')}'")
print(f"ljust(20, '.'):  '{titulo.ljust(20, '.')}'")
print(f"rjust(20, '.'):  '{titulo.rjust(20, '.')}'")
print(f"zfill(5):        '{'42'.zfill(5)}'")   # '00042'


# ===========================================================================
# CAPÍTULO 7: F-STRINGS — FORMATEO MODERNO Y PROFESIONAL
# ===========================================================================

"""
Los f-strings (formatted string literals) son la forma MODERNA y
RECOMENDADA de formatear strings en Python 3.6+.

Son más rápidos, más legibles y más potentes que las alternativas.
"""

print("\n" + "=" * 60)
print("=== F-STRINGS — FORMATEO PROFESIONAL ===")
print("=" * 60)

nombre = "José"
edad = 28
salario = 45000.50

# Básico
print(f"Nombre: {nombre}, Edad: {edad}")

# Expresiones completas dentro de {}
print(f"Edad en 5 años: {edad + 5}")
print(f"Nombre en mayúsculas: {nombre.upper()}")
print(f"Es adulto: {edad >= 18}")

# ─── ESPECIFICADORES DE FORMATO ───
print("\n--- Especificadores de formato ---")

# Ancho y alineación
print(f"{'Izquierda':<20}|")     # alinear izquierda
print(f"{'Derecha':>20}|")       # alinear derecha
print(f"{'Centrado':^20}|")      # centrar
print(f"{'Relleno':*^20}|")      # centrar con relleno

# Números
pi = 3.14159265358979
print(f"\nPi: {pi}")
print(f"Pi 2 decimales: {pi:.2f}")
print(f"Pi 10 decimales: {pi:.10f}")
print(f"Pi notación científica: {pi:.2e}")
print(f"Pi como porcentaje: {pi:.2%}")  # 314.16%
print(f"Salario con comas: {salario:,.2f}")

# Enteros
num = 42
print(f"\n{num} en binario:  {num:b}")
print(f"{num} en octal:    {num:o}")
print(f"{num} en hex:      {num:x}")
print(f"{num} en hex (may):{num:X}")
print(f"{num} con relleno: {num:08d}")  # 00000042

# ─── F-STRING DEBUG (Python 3.8+) ───
print("\n--- Debug con f-strings (= syntax) ---")
x = 42
lista = [1, 2, 3]
print(f"{x = }")              # x = 42
print(f"{lista = }")          # lista = [1, 2, 3]
print(f"{len(lista) = }")     # len(lista) = 3
print(f"{x * 2 = }")         # x * 2 = 84

"""
El operador = en f-strings es ORO PURO para debugging:
En vez de:
    print(f"loss: {loss}")
    print(f"lr: {lr}")
    print(f"epoch: {epoch}")

Puedes hacer:
    print(f"{loss = :.4f}, {lr = :.6f}, {epoch = }")
"""

# ─── F-STRINGS MULTILÍNEA ───
print("\n--- F-strings multilínea ---")

modelo = "GPT-4"
tokens = 128000
coste = 0.03

reporte = (
    f"Modelo: {modelo}\n"
    f"Contexto: {tokens:,} tokens\n"
    f"Coste: ${coste:.2f}/1K tokens\n"
    f"Coste 1M tokens: ${coste * 1000:.2f}"
)
print(reporte)

# ─── COMPARACIÓN CON OTROS MÉTODOS DE FORMATEO ───
print("\n--- Comparación de métodos ---")

nombre = "Python"
version = 3.13

# Método 1: concatenación (❌ feo y lento)
print("Hola, " + nombre + " " + str(version))

# Método 2: % formatting (❌ antiguo, estilo C)
print("Hola, %s %.1f" % (nombre, version))

# Método 3: .format() (⚠️ verboso pero aún válido)
print("Hola, {} {:.1f}".format(nombre, version))

# Método 4: f-string (✅ RECOMENDADO)
print(f"Hola, {nombre} {version:.1f}")

"""
SIEMPRE usa f-strings salvo:
  - Necesitas un template reutilizable → usa .format() o Template
  - Estás en Python < 3.6 → usa .format() (raro en 2026)
"""


# ===========================================================================
# CAPÍTULO 8: STRINGS Y BYTES — LA FRONTERA
# ===========================================================================

"""
En Python 3 hay una distinción ESTRICTA entre:
  - str:   texto (secuencia de caracteres Unicode)
  - bytes: datos binarios (secuencia de bytes 0-255)

NO son intercambiables. NO puedes mezclarlos sin convertir.
"""

print("\n=== STRINGS vs BYTES ===")

texto = "Hola, 世界"           # str
binario = b"Hello, World"       # bytes (solo ASCII)

print(f"type(texto):   {type(texto)}")     # <class 'str'>
print(f"type(binario): {type(binario)}")   # <class 'bytes'>

# str → bytes: .encode()
encoded = texto.encode('utf-8')
print(f"\n'{texto}' → {encoded}")
print(f"Longitud str:   {len(texto)} caracteres")
print(f"Longitud bytes: {len(encoded)} bytes")

# bytes → str: .decode()
decoded = encoded.decode('utf-8')
print(f"\n{encoded} → '{decoded}'")

# Error al mezclar:
try:
    resultado = texto + binario  # TypeError
except TypeError as e:
    print(f"\nError al mezclar str + bytes: {e}")

"""
CUÁNDO VES BYTES EN IA:
1. Leyendo archivos binarios (imágenes, audio, modelos .pt)
2. Comunicación HTTP (las APIs envían bytes, no strings)
3. Serialización (pickle, protobuf, msgpack)
4. Archivos de datos comprimidos (.gz, .parquet)
5. Tokenizadores a nivel de byte (BPE de GPT usa bytes)

REGLA:
  - Texto para humanos → str
  - Datos para máquinas → bytes
  - Convertir siempre con encode/decode
"""


# ===========================================================================
# CAPÍTULO 9: OPERACIONES ÚTILES CON STRINGS
# ===========================================================================

print("\n=== OPERACIONES ÚTILES ===")

# Repetición
separador = "-" * 40
print(separador)

# Pertenencia
print(f"'ML' in 'Machine Learning': {'ML' in 'Machine Learning'}")

# Longitud
print(f"len('artificial'): {len('artificial')}")

# Reversión (con slicing)
print(f"'python'[::-1]: {'python'[::-1]}")

# Contar caracteres
from collections import Counter
texto = "abracadabra"
conteo = Counter(texto)
print(f"\nConteo de '{texto}': {dict(conteo)}")
# {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}

"""
Counter es FUNDAMENTAL para NLP:
  - Contar frecuencia de palabras (bag of words)
  - Encontrar las N palabras más comunes
  - Estadísticas de vocabulario
  
  palabras = texto.split()
  frecuencias = Counter(palabras)
  top_10 = frecuencias.most_common(10)
"""


# ===========================================================================
# CAPÍTULO 10: STRINGS EN NLP — PREPROCESAMIENTO DE TEXTO
# ===========================================================================

"""
En NLP (Natural Language Processing), el preprocesamiento de texto
es el PRIMER PASO de cualquier pipeline. Aquí van las operaciones
más comunes que harás como Ingeniero de IA:
"""

print("\n=== PREPROCESAMIENTO PARA NLP ===")

texto_sucio = """
   ¡Este es un EJEMPLO de texto SUCIO!!! 
   Tiene    espacios    múltiples,   MAYÚSCULAS,
   signos de puntuación!!!... y     tabs\t\t\taquí.
"""

# 1. Eliminar espacios extremos
limpio = texto_sucio.strip()
print(f"1. strip():\n   '{limpio[:50]}...'")

# 2. Normalizar a minúsculas
limpio = limpio.casefold()
print(f"2. casefold():\n   '{limpio[:50]}...'")

# 3. Normalizar espacios múltiples
limpio = " ".join(limpio.split())
print(f"3. Normalizar espacios:\n   '{limpio[:60]}...'")

# 4. Eliminar puntuación
import string
tabla_traduccion = str.maketrans("", "", string.punctuation + "¡¿")
sin_puntuacion = limpio.translate(tabla_traduccion)
print(f"4. Sin puntuación:\n   '{sin_puntuacion[:60]}...'")

# 5. Tokenización básica (por espacios)
tokens = sin_puntuacion.split()
print(f"5. Tokens: {tokens[:8]}...")
print(f"   Total tokens: {len(tokens)}")

# 6. Eliminar stopwords (palabras muy comunes sin significado)
stopwords_es = {"de", "un", "es", "y", "el", "la", "en", "que", "los",
                "del", "las", "se", "con", "no", "una", "su", "para",
                "por", "al", "este", "como", "más", "pero", "sus",
                "le", "ya", "o", "fue", "este", "ha", "sí", "tiene",
                "aquí", "esto", "a"}

tokens_filtrados = [t for t in tokens if t not in stopwords_es]
print(f"6. Sin stopwords: {tokens_filtrados[:8]}...")
print(f"   Reducción: {len(tokens)} → {len(tokens_filtrados)} tokens")

"""
NOTA IMPORTANTE:
Este preprocesamiento "manual" es educativo, pero en producción
usarás librerías especializadas:

  - spaCy: preprocesamiento industrial-grade
  - NLTK: clásico para NLP académico
  - Hugging Face tokenizers: tokenizadores de LLMs (BPE, WordPiece)

Los tokenizadores de LLMs NO hacen este preprocesamiento.
Un LLM como GPT-4 recibe el texto TAL CUAL (con mayúsculas,
puntuación, etc.) porque su tokenizador maneja todo internamente.

Pero para ML clásico (bag of words, TF-IDF) SÍ necesitas limpiar.
"""


# ===========================================================================
# CAPÍTULO 11: STRING FORMAT MINI-LANGUAGE — REFERENCIA RÁPIDA
# ===========================================================================

"""
Los especificadores de formato siguen esta sintaxis:
  {valor:[[fill]align][sign][#][0][width][grouping][.precision][type]}

TYPES MÁS USADOS:
  d  → entero decimal
  f  → float con punto decimal
  e  → notación científica
  %  → porcentaje
  b  → binario
  x  → hexadecimal
  s  → string (default)
"""

print("\n=== FORMAT MINI-LANGUAGE ===")

# Tabla de referencia con ejemplos
valor_int = 42
valor_float = 3.14159
valor_pct = 0.8567

print(f"  {'Formato':<20} {'Resultado':<20} {'Descripción'}")
print(f"  {'-'*20} {'-'*20} {'-'*30}")
print(f"  {{:d}}                {valor_int:d:<20} Entero")
print(f"  {{:05d}}              {valor_int:05d:<20} Con ceros")
print(f"  {{:+d}}               {valor_int:+d:<20} Con signo")
print(f"  {{:.2f}}              {valor_float:.2f:<20} 2 decimales")
print(f"  {{:.6f}}              {valor_float:.6f:<20} 6 decimales")
print(f"  {{:10.2f}}            {valor_float:10.2f:<20} Ancho 10")
print(f"  {{:.2e}}              {valor_float:.2e:<20} Científica")
print(f"  {{:.2%}}              {valor_pct:.2%:<20} Porcentaje")
print(f"  {{:,}}                {1234567:,:<20} Separador miles")
print(f"  {{:_}}                {1234567:_:<20} Separador _")
print(f"  {{:b}}                {valor_int:b:<20} Binario")
print(f"  {{:x}}                {valor_int:x:<20} Hexadecimal")
print(f"  {{:#x}}               {valor_int:#x:<20} Hex con 0x")

"""
PATRÓN MUY ÚTIL EN IA — logging de entrenamiento:

  for epoch in range(100):
      loss = train_epoch()
      acc = evaluate()
      print(f"Epoch {epoch:3d}/{100} | "
            f"Loss: {loss:.4f} | "
            f"Acc: {acc:.2%} | "
            f"LR: {lr:.2e}")

  # Output:
  # Epoch   1/100 | Loss: 2.3026 | Acc: 10.42% | LR: 1.00e-03
  # Epoch  50/100 | Loss: 0.1234 | Acc: 95.23% | LR: 5.00e-04
"""


# ===========================================================================
# CAPÍTULO 12: string.Template Y PLANTILLAS
# ===========================================================================

from string import Template

print("\n=== string.Template ===")

# Template usa $variable en vez de {variable}
tmpl = Template("Modelo: $modelo, Accuracy: $acc%")
resultado = tmpl.substitute(modelo="BERT", acc=95.3)
print(f"  {resultado}")

# safe_substitute no da error si falta una variable
resultado_safe = tmpl.safe_substitute(modelo="GPT")
print(f"  safe_substitute: {resultado_safe}")

"""
¿Cuándo usar Template en vez de f-strings?

  f-strings:  para formateo en código que TÚ controlas
  Template:   para plantillas que vienen de FUERA (usuario, config, BD)

Template es más SEGURO porque no ejecuta código arbitrario:
  f"{__import__('os').system('rm -rf /')}"   ← ¡PELIGROSO!
  Template("$comando").substitute(comando=...)  ← seguro

En IA:
  - Plantillas de prompts para LLMs
  - Formateo de respuestas de APIs
  - Configuración de logging
"""


# ===========================================================================
# CAPÍTULO 13: PATRONES DE STRINGS EN PRODUCCIÓN
# ===========================================================================

print("\n=== PATRONES DE PRODUCCIÓN ===")

# ─── Multiline strings limpias ───
# Cuando necesitas strings largos sin indentación extra
from textwrap import dedent

prompt = dedent("""\
    Eres un asistente de IA especializado en Python.
    Tu objetivo es ayudar al usuario con:
    - Debugging de código
    - Optimización de rendimiento
    - Mejores prácticas
    Responde siempre en español.""")

print(f"  Prompt (sin indentación):\n{prompt}")

# ─── Construcción eficiente de strings ───
# Cuando necesitas construir strings grandes en bucles

# Método 1: lista + join (RECOMENDADO)
partes = []
for i in range(5):
    partes.append(f"Epoch {i}: loss={0.5/(i+1):.4f}")
log = "\n".join(partes)
print(f"\n  Log:\n{log}")

# Método 2: io.StringIO para strings muy grandes
import io
buffer = io.StringIO()
for i in range(5):
    buffer.write(f"Batch {i}: ")
    buffer.write(f"procesado\n")
resultado = buffer.getvalue()
print(f"\n  Buffer:\n{resultado.strip()}")


# ===========================================================================
# RESUMEN Y SIGUIENTE ARCHIVO
# ===========================================================================

"""
LO QUE HAS APRENDIDO:

1. Strings son secuencias INMUTABLES de caracteres Unicode
2. Python 3 usa Unicode internamente, UTF-8 para archivos
3. ord()/chr() para convertir entre caracteres y code points
4. Indexación [i] y slicing [inicio:fin:paso]
5. join() es MUCHO más rápido que concatenación en bucle
6. Métodos esenciales: split, join, strip, replace, find, count
7. casefold() > lower() para texto multilingüe
8. F-strings: la forma moderna y recomendada de formatear
9. str vs bytes: texto vs binario, nunca mezclar
10. Preprocesamiento de texto: strip → casefold → split → filter
11. Regex para patrones complejos
12. Format mini-language para control preciso de formato
13. string.Template para plantillas seguras
14. textwrap.dedent para strings multilínea limpias

CONEXIÓN CON IA:
- Tokenización (cómo los LLMs dividen texto) depende de Unicode
- Limpieza de datos textuales es el 80% del trabajo de NLP
- F-strings para logging durante entrenamiento
- bytes para archivos binarios (modelos, imágenes)
- Encoding importa para modelos multilingües
- Template para prompts de LLMs en producción

ARCHIVO SIGUIENTE: 05_booleanos_logica_y_control.py
→ Booleanos en profundidad
→ Operadores lógicos y cortocircuito
→ Condicionales (if/elif/else)
→ Match/case (Python 3.10+)
→ Operador ternario
→ Truthiness aplicada a flujo de control
"""

