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

var1_type = ''
var1_value = ''
comparacion = ''
var2_type = ''
var2_value = ''


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
        #Estamos haciendo un 
        variables(token)
        # print(token)
        checkLoop(token)
        if token.type == 'FINISH':
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
                print("Error in line", token.lineno,
                      ": Syntax error, assign variable")
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

    #DANIIIIIprint('\nInside the MEV function\n')

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
            if token.type != ';' or if_flag != False:
                print("Error in line", token.lineno, ": Syntax error, MEV")
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
                # DANIIIIprint('\nDani Rojas\n')
                modify_existing_varaible_flag = Tru`e
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

    if if_flag == True or while_loop_flag == True:
        checkConditional(token)
    else:
        if token.type == 'IF':
            if_flag = True
            print(if_flag, 'current value')
        elif token.type == 'WHILE':
            while_loop_flag = True


def checkConditional(token):
    global var1_type
    global var1_value
    global comparacion
    global var2_type
    global var2_value
    global state
    # if token.type == 'BOOL_TYPE':
    #    conditional_op_flag = True
    # Regresar
    # Encontrar todas las variables y operador
    # Recibir primera variable

    # 0. Esperamos un parentesis izquierdo
    if state == 0:
        if token.type == '(':
            state += 1
        else:
            print("ERROR: Esperaba un (")

    # 1. Espero una variable
    elif state == 1:
        # A ver, que variable / valor estamos esperando ?
        if token.type == 'INT_TYPE' or token.type == 'FLOAT_TYPE':
            var1_type = token.type
            var1_value = token.value
            state += 1
        elif token.type == 'BOOL_TYPE':
            var1_type = token.type
            var1_value = token.value
            state += 1
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in symbol_table.keys():
                print("ID exists! : ", symbol_table[token.value])
                var1_type = token.type
                var1_value = token.value
                state += 1
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)
        else:
            print("ERROR: Esperaba un valor / variable primer lugar")
            sys.exit(2)

    # 2. Espero una operacion logica
    elif state == 2:
        if token.type == 'EQ' or token.type == 'LE' or token.type == 'GE' or token.type == 'GT' or token.type == 'LT' or token.type == 'NE':
            comparacion = token.type
            state += 1
        elif token.type == ')':
            state = 5
        else:
            print("Error in line", token.lineno, ": Syntax error", token.value)
            sys.exit(2)

    # 3. Espero mi segunda variable
    elif state == 3:
     # A ver, que variable / valor estamos esperando ?
        if token.type == 'INT_TYPE' or token.type == 'FLOAT_TYPE':
            if checkValue(token.value, var1_type):
                var2_type = token.type
                var2_value = token.value
                state += 1
            else:
                print("ERROR: No son del mismo tipo")
                sys.exit(2)
        elif token.type == 'BOOL_TYPE':
            if checkValue(token.value, var1_type):
                var2_type = token.type
                var2_value = token.value
                state += 1
            else:
                print("ERROR: No son del mismo tipo")
                sys.exit(2)
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in symbol_table.keys():
                print("ID exists! : ", symbol_table[token.value])
                if checkValue(token.value, var1_type):
                    var2_type = token.type
                    var2_value = token.value
                    state += 1
                else:
                    print("ERROR: No son del mismo tipo, pelas")
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)
        else:
            print("ERROR: Esperaba un valor / variable segundo lugar")
            sys.exit(2)

    # Ahora espero cerrar la comparacion
    elif state == 4:
        if token.type == ')':
            state += 1
        else:
            print("ERROR: Esperaba un )")
            sys.exit(2)

    # Hacer la comparacion, ver si es valida, que te regresa y guardarla en diccionario (poner si vas a empezar if o while)
    # Resetear todas las banderas declaradas
    # {'IF': var1 {TYPE: 'INT_TYPE', 'value': 100}, 'var2': {'type': 'INT_TYPE', 'value': 110}, OPERATION}
    elif state == 5:
        if logicalOperations(var1_value, var2_value, comparacion):
            print('Si cumple')
        else:
            print('Chole con tus quejas')


def logicalOperations(var1, var2, operator):
    """ 
    Additional information:

    EQ -> r'=='

    LE -> r'<='

    LT -> r'<'

    GE -> r'>='

    GT -> r'>'

    NE -> r'!='
    """

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

""" 
    TODO:
        * Arreglar operaciones matematicas (pikachu = x 10);
        * Diferenciar entre variables
        * Pura declaracion de arreglos (se pueden manejar como las listas de Python)
            * Si se hace eso, puede afectar la tabla de simbolos 
 """


""" 
Token(type='START', value='battle_start', lineno=1, index=0)
Token(type=';', value=';', lineno=1, index=12)
pass
Token(type='INT_TYPE', value='pikachu', lineno=2, index=14)
Token(type='ID', value='x', lineno=2, index=22)
Token(type='ASSIGN', value='=', lineno=2, index=24)
Token(type='INTEGER', value=0, lineno=2, index=26)
Token(type=';', value=';', lineno=2, index=27)
Finished! x INT_TYPE 0
{'x': {'type': 'INT_TYPE', 'value': 0}}
pass
Token(type='INT_TYPE', value='pikachu', lineno=3, index=29)
Token(type='ID', value='end', lineno=3, index=37)
Token(type='ASSIGN', value='=', lineno=3, index=41)
Token(type='INTEGER', value=10, lineno=3, index=43)
Token(type=';', value=';', lineno=3, index=45)
Finished! end INT_TYPE 10
{'x': {'type': 'INT_TYPE', 'value': 0}, 'end': {'type': 'INT_TYPE', 'value': 10}}
pass
Token(type='IF', value='if_i_choose_you', lineno=4, index=47)
pass
Token(type='(', value='(', lineno=4, index=63)
pass
Token(type='ID', value='x', lineno=4, index=64)
Token(type='LE', value='<=', lineno=4, index=66)
Syntax error mod 0

{'IF': {'var1': VALUE, 'var2': VALUE, 'type': 'TIPO_OPERACION'}}
 """
