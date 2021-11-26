import sys
import GlobalVariables

def resetFlags():
    GlobalVariables.assign_variable_flag = False
    GlobalVariables.modify_existing_varaible_flag = False
    GlobalVariables.type_flag = ''
    GlobalVariables.state = 0
    GlobalVariables.variable_state = 0
    GlobalVariables.current_variable_ID = ''
    GlobalVariables.current_variable_value = ''
    GlobalVariables.if_new_variable_flag = False
    GlobalVariables.if_modify_variable_flag = False
    GlobalVariables.if_array_flag = False

def modify_existing_variable(token):
    
    # Confirmar asignacion
    if GlobalVariables.variable_state == 0:
        # Validacion
        if token.type == 'ASSIGN':
            GlobalVariables.variable_state += 1
        else:
            print('Syntax error, MEV')
            sys.exit(2)

    # Esperar ID o un valor
    elif GlobalVariables.variable_state == 1:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER' or token.type == 'CHAR' or token.type == 'BOOL':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, GlobalVariables.type_flag):
            # 2. Asignar esa variable
                GlobalVariables.current_variable_value = token.value
                GlobalVariables.variable_state += 1
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
                    GlobalVariables.variable_state += 1
                else:
                    print('Error in line',token.lineno,': Variable type', GlobalVariables.type_flag, 'doesnt support value: ', GlobalVariables.symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line",token.lineno,":  Variable ",token.value,' is not defined. 1')
                sys.exit(2)

    elif GlobalVariables.variable_state == 2:
        # Si el usuario quiere hacer una operacion durante asignacion
        if token.type == 'PLUS' or token.type == 'MINUS' or token.type == 'TIMES' or token.type == 'DIVIDE' or token.type == 'MOD':
            # Si tenemos BOOL o CHAR, tirar error porque no hace sentido hacer operaciones
            if GlobalVariables.type_flag == 'BOOL_TYPE' or GlobalVariables.type_flag == 'CHAR_TYPE':
                print("Error in line",token.lineno,":  No se pueden hacer operaciones aritmeticas en variables tipo ",GlobalVariables.type_flag)
            # Estamos trabajando con un valor numerico, guardamos que tipo de operacion es.
            else:
                GlobalVariables.current_operator = token.type
                GlobalVariables.variable_state += 1
        else:
            if token.type != ';':
                print("Error in line",token.lineno,": Syntax error")
                sys.exit(2)

    # Ya tenemos la operacion, ahora el valor
    elif GlobalVariables.variable_state == 3:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, GlobalVariables.type_flag):
            # 2. Asignar esa variable
                GlobalVariables.current_variable_value = arithmetic(GlobalVariables.current_variable_value, token.value, GlobalVariables.current_operator)
                GlobalVariables.variable_state -= 1 # Regresamos a esperar otra operacion
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
                    GlobalVariables.variable_state -= 1 # Regresamos a esperar otra operacion
                else:
                    print('Error in line',token.lineno,': Variable type', GlobalVariables.type_flag, 'doesnt support value: ', GlobalVariables.symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line",token.lineno,":  Variable ",token.value,' is not defined. 2')
                sys.exit(2)

def variables(token):
    print('Token recieved in variables', token)
        # If we know we are assigning a variable:
    if token.type == ';':
        if GlobalVariables.assign_variable_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.if_new_variable_flag == True or GlobalVariables.if_modify_variable_flag == True or GlobalVariables.if_array_flag == True:
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

    if GlobalVariables.assign_variable_flag == True or GlobalVariables.if_new_variable_flag == True:
        print('Sending token to assign variable')
        assign_variable(token)
    
    elif GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.if_modify_variable_flag == True:
        modify_existing_variable(token)
    
    # Empezamos gramatica Array
    elif GlobalVariables.assign_array_flag == True or GlobalVariables.if_array_flag == True:
        assign_array.assign_array_variable(token)
        
    else: # We got a new token and don't know what to do with it
        if token.type == 'FLOAT_TYPE' or token.type == 'INT_TYPE' or token.type == 'CHAR_TYPE' or token.type == 'BOOL_TYPE':
            
            # Si estamos dentro del if...
            if GlobalVariables.if_flag == True:
                GlobalVariables.if_new_variable_flag = True
            else:
                GlobalVariables.type_flag = token.type
                GlobalVariables.assign_variable_flag = True
        
        # Ah fuck me es un arreglo
        elif token.type == 'ARR':

            if GlobalVariables.if_flag == True:
                GlobalVariables.if_array_flag = True
                GlobalVariables.type_flag = token.type
            else:
                GlobalVariables.type_flag = token.type
                GlobalVariables.assign_array_flag = True

        # What about we want to modify an existing variable? Maybe its a function
        elif token.type == 'ID':
            # First we check if the variable already exists
            if checkIfVariableIsDefined(token):
                # Variable exists! yay Lets check if its a function

                if GlobalVariables.symbol_table[token.value]['type'] == 'FUNC':
                    print('Im a function!!!')
                    

                else:
                    
                     # Si estamos dentro del if...
                    if GlobalVariables.if_flag == True:
                        GlobalVariables.if_modify_variable_flag = True
                        # Guardar mi variable en mis flags
                        GlobalVariables.type_flag = GlobalVariables.symbol_table[token.value]['type']
                        GlobalVariables.current_variable_ID = token.value
                        GlobalVariables.current_variable_value = GlobalVariables.symbol_table[token.value]['value']
                    else:
                        GlobalVariables.modify_existing_varaible_flag = True
                        # Guardar mi variable en mis flags
                        GlobalVariables.type_flag = GlobalVariables.symbol_table[token.value]['type']
                        GlobalVariables.current_variable_ID = token.value
                        GlobalVariables.current_variable_value = GlobalVariables.symbol_table[token.value]['value']

        else:
            print('pass')

def checkLoop(token):
    # print("\nWhile flag Status: ", GlobalVariables.while_loop_flag,"If flag status: ", GlobalVariables.if_flag, '\n')
    if GlobalVariables.if_flag == True or GlobalVariables.while_loop_flag == True:
        if GlobalVariables.if_flag == True:
            loopAndConditionalAnalysis.checkConditional(token)
            # print('Sending to loopAndConditionalAnalysis file (IF/ELSE)')
        elif GlobalVariables.while_loop_flag == True:
            # print('Sending to loopAndConditionalAnalysis file (WHILE)')
            # print('Sending token', token, 'to WHILE')
            loopAndConditionalAnalysis.whileAnalysis(token)
    else:
        if token.type == 'IF':
            print('Checking IF statement')
            GlobalVariables.if_flag = True
            # print(GlobalVariables.if_flag, 'current value')
        elif token.type == 'WHILE':
            print('Checking WHILE loop')
            GlobalVariables.while_loop_flag = True
            # print(GlobalVariables.while_loop_flag, 'current value')

def checkIfVariableIsDefined(token):
    if token.value in GlobalVariables.symbol_table.keys():
        return True
    else:
        print("Error in line",token.lineno,":  Variable ",token.value,' is not defined. 3')
        sys.exit(2)

def checkIfVariableIsNOTDefined(token):
    if token.value in GlobalVariables.symbol_table.keys():
        print("Error in line",token.lineno,":  Variable ",token.value,' is not defined. 3')
        sys.exit(2)
    else:
        return True

def assign_variable(token):
    print('state', GlobalVariables.variable_state)
    # Guardamos ID
    if GlobalVariables.variable_state == 0:
        # Validacion
        if token.type == 'ID':
            # Validar que no exista el ID
            if token.value in GlobalVariables.symbol_table.keys():
                print("Error in line",token.lineno,":  Variable ",token.value,' is already defined.')
                sys.exit(2)
            else:
                GlobalVariables.current_variable_ID = token.value
                GlobalVariables.variable_state += 1
        else:
            print('Syntax error')
            sys.exit(2)

    # Confirmar asignacion
    elif GlobalVariables.variable_state == 1:
        # Validacion
        if token.type == 'ASSIGN':
            GlobalVariables.variable_state += 1
        else:
            print('Syntax error')
            sys.exit(2)

    # Esperar ID o un valor
    elif GlobalVariables.variable_state == 2:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER' or token.type == 'CHAR' or token.type == 'BOOL':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, GlobalVariables.type_flag):
            # 2. Asignar esa variable
                GlobalVariables.current_variable_value = token.value
                GlobalVariables.variable_state += 1
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
                    GlobalVariables.variable_state += 1
                else:
                    print('Error in line',token.lineno,': Variable type', GlobalVariables.type_flag, 'doesnt support value: ', GlobalVariables.symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line",token.lineno,":  Variable ",token.value,' is not defined. 4')
                sys.exit(2)

    elif GlobalVariables.variable_state == 3:
        # Si el usuario quiere hacer una operacion durante asignacion
        if token.type == 'PLUS' or token.type == 'MINUS' or token.type == 'TIMES' or token.type == 'DIVIDE' or token.type == 'MOD':
            # Si tenemos BOOL o CHAR, tirar error porque no hace sentido hacer operaciones
            if GlobalVariables.type_flag == 'BOOL_TYPE' or GlobalVariables.type_flag == 'CHAR_TYPE':
                print("Error in line",token.lineno,":  No se pueden hacer operaciones aritmeticas en variables tipo ",GlobalVariables.type_flag)
            # Estamos trabajando con un valor numerico, guardamos que tipo de operacion es.
            else:
                GlobalVariables.current_operator = token.type
                GlobalVariables.variable_state += 1
        else:
            if token.type != ';':
                print("Error in line",token.lineno,": Syntax error")
                sys.exit(2)

    # Ya tenemos la operacion, ahora el valor
    elif GlobalVariables.variable_state == 4:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, GlobalVariables.type_flag):
            # 2. Asignar esa variable
                GlobalVariables.current_variable_value = arithmetic(GlobalVariables.current_variable_value, token.value, GlobalVariables.current_operator)
                GlobalVariables.variable_state -= 1 # Regresamos a esperar otra operacion
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
                    GlobalVariables.variable_state -= 1 # Regresamos a esperar otra operacion
                else:
                    print('Error in line',token.lineno,': Variable type', GlobalVariables.type_flag, 'doesnt support value: ', GlobalVariables.symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line",token.lineno,":  Variable ",token.value,' is not defined. 5')
                sys.exit(2)


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