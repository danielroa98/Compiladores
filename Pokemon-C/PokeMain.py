import getopt
import sys
import PokeLexer

if __name__ == '__main__':
    inputFile = ''
    fileData = ''

    userInputs = sys.argv[1:]
    try:
        args, values = getopt.getopt(userInputs, 'hi:', ['help', 'ifile'])
        for arg, value in args:
            # print(arg, value)
            if arg in ('-h', '--help'):
                print(
                    'In order to use Pokemon-C, run the following command.\npython3 PokeMain.py -i <path/to/inputFile>')
                sys.exit(2)
            elif arg in ('-i', '--ifile'):
                print('Using file located in', value, 'as the current input.')
                inputFile = open(value, "r")
                fileData = inputFile.read()

    except getopt.GetoptError:
        print('Run main.py -i <inputfile>')
        sys.exit(2)

    # print(fileData)
    PokeLexer.lexerStart(fileData)
