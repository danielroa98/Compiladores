import sys

# Symbol Table Class


class Variable:
    def __init__(self, id, type, value):
        self.id = id
        self.type = type
        self.value = value


# Symbol Table
symbol_table = {}

# Global variables | Flags
start_flag = False
end_flag = False

# Flags for Variables
assign_variable_flag = False
type_flag = ''
state = 0
current_variable_ID = ''
current_variable_value = ''
current_operator = ''
modify_existing_varaible_flag = False
conditional_op_flag = False
if_flag = False
while_loop_flag = False
leftparenthesis = False
rightparenthesis = False
varComparator1 = ''
varComparator2 = ''
varCompFlag1 = False
varCompFlag2 = False
vars_to_compare = []
logcial_operator = ''


def init(token):
    programInit(token)


def resetFlags():
    global assign_variable_flag
    global type_flag
    global state
    global current_variable_ID
    global current_variable_value
    global modify_existing_varaible_flag

    assign_variable_flag = False
    modify_existing_varaible_flag = False
    type_flag = ''
    state = 0
    current_variable_ID = ''
    current_variable_value = ''


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
    # if 'START' in token:
    if token.type == 'START':
        # print(start_flag)
        if start_flag == True:
            printErr(token, 2)
        else:
            start_flag = True
            return
            # print("Changing the start flag:", start_flag)
    elif start_flag == True:
        variables(token)
        if token.type == 'IF' or token.type == 'WHILE' or if_flag == True or while_loop_flag == True:
            checkLoop(token)
            checkConditional(token)
        # if 'FINISH' in token:
        elif token.type == 'FINISH':
            programEnd(token)
    else:
        printErr(token, 1)

# Funcion para checar si el valor cumple con el tipo de la variable


def checkValue(value, type):
    if type == 'INT_TYPE' and isinstance(value, int):
        return True
    elif type == 'FLOAT_TYPE' and isinstance(value, float):
        return True
    else:
        return False


def arithmetic(val1, val2, type):
    if type == 'PLUS':
        return val1+val2
    elif type == 'MINUS':
        return val1-val2
    elif type == 'TIMES':
        return val1*val2
    elif type == 'DIVIDE':
        return val1/val2
    elif type == 'MOD':
        return val1 % val2


def assign_variable(token):
    global type_flag
    global state
    global current_variable_ID
    global current_variable_value
    global symbol_table
    global current_operator

    # Guardamos ID
    if state == 0:
        # Validacion
        if token.type == 'ID':
            current_variable_ID = token.value
            state += 1
        else:
            print('Syntax error 0')

    # Confirmar asignacion
    elif state == 1:
        # Validacion
        if token.type == 'ASSIGN':
            state += 1
        else:
            print('Syntax error 1')
            sys.exit(2)

    # Esperar ID o un valor
    elif state == 2:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, type_flag):
                # 2. Asignar esa variable
                current_variable_value = token.value
                state += 1
            else:
                print('Error in line', token.lineno, ':  Variable type',
                      type_flag, 'doesnt support value: ', token.value)
                sys.exit(2)

        # Si nos da un ID
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in symbol_table.keys():
                print("ID exists! : ", symbol_table[token.value])
                # 2. Checar si sus tipos son compatibles
                if checkValue(symbol_table[token.value]['value'], type_flag):
                    # 2. Asignar esa variable
                    current_variable_value = symbol_table[token.value]['value']
                    state += 1
                else:
                    print('Error in line', token.lineno, ': Variable type', type_flag,
                          'doesnt support value: ', symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)

    elif state == 3:
        # Si el usuario quiere hacer una operacion durante asignacion
        if token.type == 'PLUS' or token.type == 'MINUS' or token.type == 'TIMES' or token.type == 'DIVIDE' or token.type == 'MOD':
            # Si tenemos BOOL o CHAR, tirar error porque no hace sentido hacer operaciones
            if type_flag == 'BOOL_TYPE' or type_flag == 'CHAR_TYPE':
                print("Error in line", token.lineno,
                      ":  No se pueden hacer operaciones aritmeticas en variables tipo ", type_flag)
            # Estamos trabajando con un valor numerico, guardamos que tipo de operacion es.
            else:
                current_operator = token.type
                state += 1
        else:
            if token.type != ';':
                print("Error in line", token.lineno, ": Syntax error")
                sys.exit(2)

    # Ya tenemos la operacion, ahora el valor
    elif state == 4:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, type_flag):
                # 2. Asignar esa variable
                current_variable_value = arithmetic(
                    current_variable_value, token.value, current_operator)
                state -= 1  # Regresamos a esperar otra operacion
            else:
                print('Error in line', token.lineno, ':  Variable type',
                      type_flag, 'doesnt support value: ', token.value)
                sys.exit(2)

        # Si nos da un ID
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in symbol_table.keys():
                print("ID exists! : ", symbol_table[token.value])
                # 2. Checar si sus tipos son compatibles
                if checkValue(symbol_table[token.value]['value'], type_flag):
                    # 2. Asignar esa variable
                    current_variable_value = arithmetic(
                        current_variable_value, symbol_table[token.value]['value'], current_operator)
                    state -= 1  # Regresamos a esperar otra operacion
                else:
                    print('Error in line', token.lineno, ': Variable type', type_flag,
                          'doesnt support value: ', symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)


def checkIfVariableIsDefined(token):
    global symbol_table
    if token.value in symbol_table.keys():
        return True
    else:
        print("Error in line", token.lineno, ":  Variable ",
              token.value, ' is not defined.')
        sys.exit(2)


def modify_existing_variable(token):
    global type_flag
    global state
    global current_variable_ID
    global current_variable_value
    global symbol_table
    global current_operator

    # Confirmar asignacion
    if state == 0:
        # Validacion
        if token.type == 'ASSIGN':
            state += 1
        else:
            print('Syntax error mod 0')
            sys.exit(2)

    # Esperar ID o un valor
    elif state == 1:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, type_flag):
                # 2. Asignar esa variable
                current_variable_value = token.value
                state += 1
            else:
                print('Error in line', token.lineno, ':  Variable type',
                      type_flag, 'doesnt support value: ', token.value)
                sys.exit(2)

        # Si nos da un ID
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in symbol_table.keys():
                print("ID exists! : ", symbol_table[token.value])
                # 2. Checar si sus tipos son compatibles
                if checkValue(symbol_table[token.value]['value'], type_flag):
                    # 2. Asignar esa variable
                    current_variable_value = symbol_table[token.value]['value']
                    state += 1
                else:
                    print('Error in line', token.lineno, ': Variable type', type_flag,
                          'doesnt support value: ', symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)

    elif state == 2:
        # Si el usuario quiere hacer una operacion durante asignacion
        if token.type == 'PLUS' or token.type == 'MINUS' or token.type == 'TIMES' or token.type == 'DIVIDE' or token.type == 'MOD':
            # Si tenemos BOOL o CHAR, tirar error porque no hace sentido hacer operaciones
            if type_flag == 'BOOL_TYPE' or type_flag == 'CHAR_TYPE':
                print("Error in line", token.lineno,
                      ":  No se pueden hacer operaciones aritmeticas en variables tipo ", type_flag)
            # Estamos trabajando con un valor numerico, guardamos que tipo de operacion es.
            else:
                current_operator = token.type
                state += 1
        else:
            if token.type != ';':
                print("Error in line", token.lineno, ": Syntax error")
                sys.exit(2)

    # Ya tenemos la operacion, ahora el valor
    elif state == 3:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, type_flag):
                # 2. Asignar esa variable
                current_variable_value = arithmetic(
                    current_variable_value, token.value, current_operator)
                state -= 1  # Regresamos a esperar otra operacion
            else:
                print('Error in line', token.lineno, ':  Variable type',
                      type_flag, 'doesnt support value: ', token.value)
                sys.exit(2)

        # Si nos da un ID
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in symbol_table.keys():
                print("ID exists! : ", symbol_table[token.value])
                # 2. Checar si sus tipos son compatibles
                if checkValue(symbol_table[token.value]['value'], type_flag):
                    # 2. Asignar esa variable
                    current_variable_value = arithmetic(
                        current_variable_value, symbol_table[token.value]['value'], current_operator)
                    state -= 1  # Regresamos a esperar otra operacion
                else:
                    print('Error in line', token.lineno, ': Variable type', type_flag,
                          'doesnt support value: ', symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)


def variables(token):
    global symbol_table
    global assign_variable_flag
    global type_flag
    global current_variable_ID
    global current_variable_value
    global modify_existing_varaible_flag
    global state

    # If we know we are assigning a variable:
    if token.type == ';':
        if assign_variable_flag == True or modify_existing_varaible_flag == True:
            assign_variable(token)
            print('Finished!', current_variable_ID,
                  type_flag, current_variable_value)
            #var = Variable(current_variable_ID, type_flag, current_variable_value)
            symbol_table[current_variable_ID] = {
                "type": type_flag,
                "value": current_variable_value
            }
            #print('Variable: ',symbol_table[0].type,' ', symbol_table[0].id, ' = ', symbol_table[0].value)
            print(symbol_table)
            resetFlags()

    if assign_variable_flag == True:
        assign_variable(token)

    elif modify_existing_varaible_flag == True:
        modify_existing_variable(token)

    else:  # We got a new token and don't know what to do with it
        if token.type == 'INT_TYPE' or token.type == 'FLOAT_TYPE':
            type_flag = token.type
            assign_variable_flag = True

        # What about we want to modify an existing variable?
        elif token.type == 'ID':
            # First we check if the variable already exists
            if checkIfVariableIsDefined(token):
                # Variable exists! yay
                modify_existing_varaible_flag = True
                # Guardar mi variable en mis flags
                type_flag = symbol_table[token.value]['type']
                current_variable_ID = token.value
                current_variable_value = symbol_table[token.value]['value']

        else:
            print('pass')


def checkLoop(token):
    global conditional_op_flag
    global if_flag
    global while_loop_flag
    global leftparenthesis
    global rightparenthesis
    global logcial_operator

    if token.type == 'IF' or if_flag == True:
        if_flag = True

        if token.type == '(' or leftparenthesis == True:
            leftparenthesis = True

            if conditional_op_flag == False:
                checkConditional()
            # '(' Check open parenthesis
                # If true, next we check for a condition
                # If false we expected a (

                print('This is an if')

    elif token.type == 'WHILE' or while_loop_flag == True:
        while_loop_flag = True
        print('This is a while')


def checkConditional(token):
    global varComparator1
    global varCompFlag1
    global varComparator2
    global varCompFlag2
    global vars_to_compare
    #if token.type == 'BOOL_TYPE':
    #    conditional_op_flag = True
        #Regresar
    #Encontrar todas las variables y operador
    #Recibir primera variable
    if token.type=='INT_TYPE':
        if varCompFlag1 == False:
            varCompFlag1 = True
            varComparator1 = 'INT'
            vars_to_compare.append(token.value)
        elif varComparator2==False:
            if conditional_flag==False:
                
            varCompFlag2 = True
            varComparator2 = 'INT'
            vars_to_compare.append(token.value)
            #Call the operation
            logicalOperations(vars_to_compare, operator)
        else:
            print("Error, two values already used in the comparison")
        varComparator1=token.value

    
    


def logicalOperations(variableList, operator):
    """ 
    Additional information:

    EQ = r'=='

    LE = r'<='

    LT = r'<'

    GE = r'>='

    GT = r'>'

    NE = r'!='
    """
    global vars_to_compare

    var1 = variableList[0]
    var2 = variableList[1]
    
    #Clear variable list after declaration
    vars_to_compare.clear()

    if operator.type == 'EQ':
        if var1 == var2:
            return True
        else:
            return False
    elif operator.type == 'LE':
        if var1 <= var2:
            return True
        else:
            return False

    elif operator.type == 'LT':
        if var1 < var2:
            return True
        else:
            return False

    elif operator.type == 'GE':
        if var1 >= var2:
            return True
        else:
            return False

    elif operator.type == 'GT':
        if var1 > var2:
            return True
        else:
            return False

    elif operator.type == 'NE':
        if var1 != var2:
            return True
        else:
            return False


def programEnd(token):
    global end_flag
    print('Ending execution')
    # if 'FINISH' in token:
    if token.type == 'FINISH':
        if end_flag == True:
            printErr(token, 3)
        else:
            end_flag = True
            sys.exit(2)
    else:
        printErr(token, 4)
    # return token
