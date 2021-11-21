import sys

# Symbol Table Class
class Variable:
    def __init__(self, id, type, value):
        self.id = id
        self.type = type
        self.value = value

# Variables: 
import GlobalVariables

# Analysis functions:
import assign_array
import prints
import loopAndConditionalAnalysis
import functions
import structure

def init(token):
    programInit(token)

def resetFlags():
    GlobalVariables.assign_variable_flag = False
    GlobalVariables.modify_existing_varaible_flag = False
    GlobalVariables.type_flag = ''
    GlobalVariables.state = 0
    GlobalVariables.current_variable_ID = ''
    GlobalVariables.current_variable_value = ''

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
    #if 'START' in token:
    if token.type == 'START':
        # print(GlobalVariables.start_flag)
        if GlobalVariables.start_flag == True:
            printErr(token, 2)
        else:
            GlobalVariables.start_flag = True
            return
            # print("Changing the start flag:", GlobalVariables.start_flag)
    elif GlobalVariables.start_flag == True:
        
        if GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True or GlobalVariables.if_flag == True or GlobalVariables.declare_function_flag == True or GlobalVariables.declare_struct_flag == True:
            print('No variable detected.')
        else:
            variables(token)

        if GlobalVariables.assign_variable_flag == True or GlobalVariables.assign_array_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.if_flag == True or GlobalVariables.declare_function_flag == True or GlobalVariables.declare_struct_flag == True:
            print('No print statement detected.')
        else:
            prints.what_print(token)

        if GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True or GlobalVariables.assign_variable_flag == True or GlobalVariables.assign_array_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.declare_function_flag == True or GlobalVariables.declare_struct_flag == True:
            print('No if or while detected.')
        else:
            checkLoop(token)

        if GlobalVariables.assign_variable_flag == True or GlobalVariables.assign_array_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.if_flag == True or GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True or GlobalVariables.declare_struct_flag == True:
        #if 'FINISH' in token:
            print('No function detected.')
        else:
            functions.define_function(token)

        if GlobalVariables.assign_variable_flag == True or GlobalVariables.assign_array_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.if_flag == True or GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True:
            #if 'FINISH' in token:
            print('No structure detected.')
        else:
            structure.define_struct(token)


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
        return val1%val2

def assign_variable(token):

    # Guardamos ID
    if GlobalVariables.state == 0:
        # Validacion
        if token.type == 'ID':
            # Validar que no exista el ID
            if token.value in GlobalVariables.symbol_table.keys():
                print("Error in line",token.lineno,":  Variable ",token.value,' is already defined.')
                sys.exit(2)
            else:
                GlobalVariables.current_variable_ID = token.value
                GlobalVariables.state += 1
        else:
            print('Syntax error')
            sys.exit(2)

    # Confirmar asignacion
    elif GlobalVariables.state == 1:
        # Validacion
        if token.type == 'ASSIGN':
            GlobalVariables.state += 1
        else:
            print('Syntax error')
            sys.exit(2)

    # Esperar ID o un valor
    elif GlobalVariables.state == 2:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, GlobalVariables.type_flag):
            # 2. Asignar esa variable
                GlobalVariables.current_variable_value = token.value
                GlobalVariables.state += 1
            else:
                print('Error in line',token.lineno,':  Variable type', GlobalVariables.type_flag, 'doesnt support value: ', token.value)
                sys.exit(2)

        # Si nos da un ID
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! : ", GlobalVariables.symbol_table[token.value])
                # 2. Checar si sus tipos son compatibles
                if checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.type_flag):
                    # 2. Asignar esa variable
                    GlobalVariables.current_variable_value = GlobalVariables.symbol_table[token.value]['value']
                    GlobalVariables.state += 1
                else:
                    print('Error in line',token.lineno,': Variable type', GlobalVariables.type_flag, 'doesnt support value: ', GlobalVariables.symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line",token.lineno,":  Variable ",token.value,' is not defined.')
                sys.exit(2)

    elif GlobalVariables.state == 3:
        # Si el usuario quiere hacer una operacion durante asignacion
        if token.type == 'PLUS' or token.type == 'MINUS' or token.type == 'TIMES' or token.type == 'DIVIDE' or token.type == 'MOD':
            # Si tenemos BOOL o CHAR, tirar error porque no hace sentido hacer operaciones
            if GlobalVariables.type_flag == 'BOOL_TYPE' or GlobalVariables.type_flag == 'CHAR_TYPE':
                print("Error in line",token.lineno,":  No se pueden hacer operaciones aritmeticas en variables tipo ",GlobalVariables.type_flag)
            # Estamos trabajando con un valor numerico, guardamos que tipo de operacion es.
            else:
                GlobalVariables.current_operator = token.type
                GlobalVariables.state += 1
        else:
            if token.type != ';':
                print("Error in line",token.lineno,": Syntax error")
                sys.exit(2)

    # Ya tenemos la operacion, ahora el valor
    elif GlobalVariables.state == 4:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, GlobalVariables.type_flag):
            # 2. Asignar esa variable
                GlobalVariables.current_variable_value = arithmetic(GlobalVariables.current_variable_value, token.value, GlobalVariables.current_operator)
                GlobalVariables.state -= 1 # Regresamos a esperar otra operacion
            else:
                print('Error in line',token.lineno,':  Variable type', GlobalVariables.type_flag, 'doesnt support value: ', token.value)
                sys.exit(2)

        # Si nos da un ID
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! : ", GlobalVariables.symbol_table[token.value])
                # 2. Checar si sus tipos son compatibles
                if checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.type_flag):
                    # 2. Asignar esa variable
                    GlobalVariables.current_variable_value = arithmetic(GlobalVariables.current_variable_value, GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.current_operator) 
                    GlobalVariables.state -= 1 # Regresamos a esperar otra operacion
                else:
                    print('Error in line',token.lineno,': Variable type', GlobalVariables.type_flag, 'doesnt support value: ', GlobalVariables.symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line",token.lineno,":  Variable ",token.value,' is not defined.')
                sys.exit(2)

def checkIfVariableIsDefined(token):
    if token.value in GlobalVariables.symbol_table.keys():
        return True
    else:
        print("Error in line",token.lineno,":  Variable ",token.value,' is not defined.')
        sys.exit(2)

def modify_existing_variable(token):

    # Confirmar asignacion
    if GlobalVariables.state == 0:
        # Validacion
        if token.type == 'ASSIGN':
            GlobalVariables.state += 1
        else:
            print('Syntax error, MEV')
            sys.exit(2)

    # Esperar ID o un valor
    elif GlobalVariables.state == 1:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, GlobalVariables.type_flag):
            # 2. Asignar esa variable
                GlobalVariables.current_variable_value = token.value
                GlobalVariables.state += 1
            else:
                print('Error in line',token.lineno,':  Variable type', GlobalVariables.type_flag, 'doesnt support value: ', token.value)
                sys.exit(2)

        # Si nos da un ID
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! : ", GlobalVariables.symbol_table[token.value])
                # 2. Checar si sus tipos son compatibles
                if checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.type_flag):
                    # 2. Asignar esa variable
                    GlobalVariables.current_variable_value = GlobalVariables.symbol_table[token.value]['value']
                    GlobalVariables.state += 1
                else:
                    print('Error in line',token.lineno,': Variable type', GlobalVariables.type_flag, 'doesnt support value: ', GlobalVariables.symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line",token.lineno,":  Variable ",token.value,' is not defined.')
                sys.exit(2)

    elif GlobalVariables.state == 2:
        # Si el usuario quiere hacer una operacion durante asignacion
        if token.type == 'PLUS' or token.type == 'MINUS' or token.type == 'TIMES' or token.type == 'DIVIDE' or token.type == 'MOD':
            # Si tenemos BOOL o CHAR, tirar error porque no hace sentido hacer operaciones
            if GlobalVariables.type_flag == 'BOOL_TYPE' or GlobalVariables.type_flag == 'CHAR_TYPE':
                print("Error in line",token.lineno,":  No se pueden hacer operaciones aritmeticas en variables tipo ",GlobalVariables.type_flag)
            # Estamos trabajando con un valor numerico, guardamos que tipo de operacion es.
            else:
                GlobalVariables.current_operator = token.type
                GlobalVariables.state += 1
        else:
            if token.type != ';':
                print("Error in line",token.lineno,": Syntax error")
                sys.exit(2)

    # Ya tenemos la operacion, ahora el valor
    elif GlobalVariables.state == 3:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, GlobalVariables.type_flag):
            # 2. Asignar esa variable
                GlobalVariables.current_variable_value = arithmetic(GlobalVariables.current_variable_value, token.value, GlobalVariables.current_operator)
                GlobalVariables.state -= 1 # Regresamos a esperar otra operacion
            else:
                print('Error in line',token.lineno,':  Variable type', GlobalVariables.type_flag, 'doesnt support value: ', token.value)
                sys.exit(2)

        # Si nos da un ID
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! : ", GlobalVariables.symbol_table[token.value])
                # 2. Checar si sus tipos son compatibles
                if checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.type_flag):
                    # 2. Asignar esa variable
                    GlobalVariables.current_variable_value = arithmetic(GlobalVariables.current_variable_value, GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.current_operator) 
                    GlobalVariables.state -= 1 # Regresamos a esperar otra operacion
                else:
                    print('Error in line',token.lineno,': Variable type', GlobalVariables.type_flag, 'doesnt support value: ', GlobalVariables.symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line",token.lineno,":  Variable ",token.value,' is not defined.')
                sys.exit(2)

def variables(token):
        # If we know we are assigning a variable:
    if token.type == ';':
        if GlobalVariables.assign_variable_flag == True or GlobalVariables.modify_existing_varaible_flag == True:
            assign_variable(token)
            print('Finished!',GlobalVariables.current_variable_ID, GlobalVariables.type_flag, GlobalVariables.current_variable_value)
            #var = Variable(GlobalVariables.current_variable_ID, GlobalVariables.type_flag, GlobalVariables.current_variable_value)
            GlobalVariables.symbol_table[GlobalVariables.current_variable_ID] = {
                "type": GlobalVariables.type_flag,
                "value": GlobalVariables.current_variable_value
            }
            #print('Variable: ',GlobalVariables.symbol_table[0].type,' ', GlobalVariables.symbol_table[0].id, ' = ', GlobalVariables.symbol_table[0].value)
            print(GlobalVariables.symbol_table)
            resetFlags()

    if GlobalVariables.assign_variable_flag == True:
        assign_variable(token)
    
    elif GlobalVariables.modify_existing_varaible_flag == True:
        modify_existing_variable(token)
    
    # Empezamos gramatica Array
    elif GlobalVariables.assign_array_flag == True:
        assign_array.assign_array_variable(token)
        
    else: # We got a new token and don't know what to do with it
        if token.type == 'INT_TYPE' or token.type == 'FLOAT_TYPE':
            GlobalVariables.type_flag = token.type
            GlobalVariables.assign_variable_flag = True
        
        # Ah fuck me es un arreglo
        elif token.type == 'ARR':
            GlobalVariables.type_flag = token.type
            GlobalVariables.assign_array_flag = True

        # What about we want to modify an existing variable?
        elif token.type == 'ID':
            # First we check if the variable already exists
            if checkIfVariableIsDefined(token):
                # Variable exists! yay
                GlobalVariables.modify_existing_varaible_flag = True
                # Guardar mi variable en mis flags
                GlobalVariables.type_flag = GlobalVariables.symbol_table[token.value]['type']
                GlobalVariables.current_variable_ID = token.value
                GlobalVariables.current_variable_value = GlobalVariables.symbol_table[token.value]['value']

        else:
            print('pass')
    
def checkLoop(token):

    if GlobalVariables.if_flag == True or GlobalVariables.while_loop_flag == True:
        loopAndConditionalAnalysis.checkConditional(token)
        print('Sending to loopAndConditionalAnalysis file')
    else:
        if token.type == 'IF':
            print('Checking IF statement')
            GlobalVariables.if_flag = True
            print(GlobalVariables.if_flag, 'current value')
        elif token.type == 'WHILE':
            print('Checking WHILE loop')
            GlobalVariables.while_loop_flag = True
            print(GlobalVariables.while_loop_flag, 'current value')


def programEnd(token):
    
    print('Ending execution')
    #if 'FINISH' in token:
    if token.type == 'FINISH':
        if GlobalVariables.end_flag == True:
            printErr(token, 3)
        else:
            GlobalVariables.end_flag = True
            sys.exit(2)
    else:
        printErr(token, 4)
    # return token

