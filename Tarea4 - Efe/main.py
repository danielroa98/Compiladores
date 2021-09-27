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
finalTranslation = ''

# Currently analyzed word
currentWord = ''
seperatedSyl = []
translatedWord = []

def meterF(silaba):
    silaba = silaba[::-1]
    for index, letter in enumerate(silaba):
        if letter in vowels:
            posF = vowels.index(letter)
            silaba = silaba[::-1]
            tindex = len(silaba) - index
            trans = silaba[:tindex] + fVowels[posF] + silaba[tindex:]
            return trans

def createNewSentence(traduccion):
    finalTranslation = " ".join(translation)
    return finalTranslation

def crearF(palabra):
    currentWord = palabra
    # Seperated word into syllables and inserted them into a list
    seperatedSyl = pylabeador.syllabify(currentWord)
    for i in seperatedSyl:
        translatedWord.append(meterF(i))
    translation.append("".join(translatedWord))

def main(oracion):
    original = oracion.lower().split()
    for palabra in original:
        palabra = crearF(palabra)
        translatedWord.clear()
    # print(original)

if __name__ == '__main__':
    print('Escriba la oración que desea traducir a "F":')
    oracion = input()
    main(oracion)
    print('\nLa oración original es:\n', oracion)
    print('\nLa oración traducida es:\n',createNewSentence(translation),'\n')
