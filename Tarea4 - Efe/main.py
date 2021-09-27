""" 
    Tarea 4     -   Hablando con la F

    Daniel Roa          -   A01021960
    Antonio Junco       -   A01339695
    Sergio Hernández    -   A01025210
    Sebastián Vives     -   A01025211
"""
# Librería encargada de separar las palabras en sílabas
import pylabeador

# Declaración de las vocales para poder compararlas en las palabras
vowels = ['a', 'e', 'i', 'o', 'u']
fVowels = ['fa', 'fe', 'fi', 'fo', 'fu']

# List that contains the original sentence
original = []

# List which will contain the converted sentence
translation = []


def crearF(palabra):
    print(pylabeador.syllabify(palabra))


def main(oracion):
    original = oracion.split()
    for i in original:
        # print(i)
        crearF(i)


if __name__ == '__main__':
    print('Escriba la oración que desea traducir a "F":')
    oracion = input()
    main(oracion)
