
'''
Antonio Junco de Haas - A01339695
Luis Daniel Roa González - A01021960
Sergio Hernández Castillo - A01025210
Sebastián Gonzalo Vives Faus - A01025211

'''

import getopt
import sys
import PokeLexer
import PokeSemantics

if __name__ == '__main__':
    inputFile = ''
    fileData = ''

    userInputs = sys.argv[1:]
    try:
        args, values = getopt.getopt(userInputs, 'hi:', ['help', 'ifile'])
        for arg, value in args:
            # print(arg, value)
            if arg in ('-h', '--help'):
                print('Para comenzar a usar PokeLang, corra el siguiente comando.\npython3 PokeMain.py -i <path/al/archivo>')
                sys.exit(2)
            elif arg in ('-i', '--ifile'):
                # print('Using file located in', value, 'as the current input.')
                inputFile = open(value, "r")
                fileData = inputFile.read()
                inputFile.close()

    except getopt.GetoptError:
        print('Corra main.py -i <inputfile>')
        sys.exit(2)

    # Obtain tokens
    tokens = PokeLexer.lexerStart(fileData)
    for tok in tokens:
        #tok = str(tok)
        #print(tok)
        PokeSemantics.init(tok)
