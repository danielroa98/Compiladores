start_flag = False
end_flag = False

def init(token):
    programInit(token)


def printErr(token, errcode):
    print("Error en el token:", token)
    if errcode == 1:
        print('Error: La batalla aun no inicia.')
    elif errcode == 2:
        print('Error: La batalla ya esta iniciada.')
    elif errcode == 3:
        print('Error: La batalla ya finalizó.')
    elif errcode == 4:
        print('Error: La batalla aun no acaba.')


def programInit(token):
    global start_flag
    if 'START' in token:
        # print(start_flag)
        if start_flag == True:
            printErr(token, 2)
        else:
            start_flag = True
            # print("Changing the start flag:", start_flag)
    elif start_flag == True:
        variables(token)
        if 'FINISH' in token:
            programEnd(token)
    else:
        printErr(token, 1)


def variables(token):
    print('Token', token)
    return token


def programEnd(token):
    global end_flag
    print('Ending execution')
    if 'FINISH' in token:
        if end_flag == True:
            printErr(token, 3)
        else:
            end_flag = True
    else:
        printErr(token, 4)
    # return token


""" 
class semanticAnalyser:
    def __init__(self, token):
        self.token = token

    def programInit(token):
        print('\t')
        # if 'START' in token:
        #     if start_flag:
        #         printErr(token, 2)
        #     else:
        #         start_flag = True
        # else:
        #     printErr(token, 1)

    def variables(token):
        return token

    def programEnd(token):
        return token
 """
