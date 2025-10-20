import sys
import random

#!/usr/bin/env python3
# tesramabien.py - Código simple: imprime una o varias frases aleatorias.

FRASES = [
    "¡Hola! Que tengas un buen día.",
    "Sigue aprendiendo, paso a paso.",
    "Pequeños avances, grandes resultados.",
    "La curiosidad es el motor del código.",
    "Comete errores rápido y aprende rápido."
]

def main():
    # Si se pasa un número como primer argumento, imprime esa cantidad de frases.
    n = 1
    if len(sys.argv) > 1:
        try:
            n = max(1, int(sys.argv[1]))
        except ValueError:
            pass
    for _ in range(n):
        print(random.choice(FRASES))

if __name__ == "__main__":
    main()