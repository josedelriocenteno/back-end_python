# invertir_args.py
import sys

# sys.argv es la lista de argumentos de la línea de comandos
# sys.argv[0] = nombre del script
# sys.argv[1:] = argumentos que pasa el usuario
args = sys.argv[1:]          # me quedo solo con los argumentos
args_invertidos = args[::-1] # slicing para invertir la lista

for arg in args_invertidos:
    print(arg)