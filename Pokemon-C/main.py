import getopt
import sys


if __name__ == '__main__':
    inputFile = ''

    userInputs = sys.argv[1:]
    try:
        args, values = getopt.getopt(userInputs, 'hi:', ['help', 'ifile'])
        for arg, value in args:
            # print(arg, value)
            if arg in ('-h', '--help'):
                print(
                    'In order to use Pokemon-C, run the following command.\npython3 main.py -i <inputFile>')
            elif arg in ('-i', '--ifile'):
                inputFile = value
                print('Using file', value, 'as the current input.')

    except getopt.GetoptError:
        print('Run main.py -i <inputfile>')
        sys.exit(2)

    print(inputFile)