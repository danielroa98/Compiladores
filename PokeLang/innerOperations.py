'''
Antonio Junco de Haas - A01339695
Luis Daniel Roa González - A01021960
Sergio Hernández Castillo - A01025210
Sebastián Gonzalo Vives Faus - A01025211

'''
import GlobalVariables
import sys

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

    # Guardamos ID
    if GlobalVariables.state == 0:
        # Validacion
        if token.type == 'ID':
            # Validar que no exista el ID
            if token.value in GlobalVariables.symbol_table.keys():
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is already defined.')
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
        if token.type == 'FLOAT' or token.type == 'INTEGER' or token.type == 'CHAR' or token.type == 'BOOL':
            # 1. Checar si mi variable soporta ese tipo
            if GlobalVariables.checkValue(token.value, GlobalVariables.type_flag):
                # 2. Asignar esa variable
                GlobalVariables.current_variable_value = token.value
                GlobalVariables.state += 1
            else:
                print('Error in line', token.lineno, ':  Variable type',
                      GlobalVariables.type_flag, 'doesnt support value: ', token.value)
                sys.exit(2)

        # Si nos da un ID
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! : ",
                      GlobalVariables.symbol_table[token.value])
                # 2. Checar si sus tipos son compatibles
                if GlobalVariables.checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.type_flag):
                    # 2. Asignar esa variable
                    GlobalVariables.current_variable_value = GlobalVariables.symbol_table[
                        token.value]['value']
                    GlobalVariables.state += 1
                else:
                    print('Error in line', token.lineno, ': Variable type', GlobalVariables.type_flag,
                          'doesnt support value: ', GlobalVariables.symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)

    elif GlobalVariables.state == 3:
        # Si el usuario quiere hacer una operacion durante asignacion
        if token.type == 'PLUS' or token.type == 'MINUS' or token.type == 'TIMES' or token.type == 'DIVIDE' or token.type == 'MOD':
            # Si tenemos BOOL o CHAR, tirar error porque no hace sentido hacer operaciones
            if GlobalVariables.type_flag == 'BOOL_TYPE' or GlobalVariables.type_flag == 'CHAR_TYPE':
                print("Error in line", token.lineno,
                      ":  No se pueden hacer operaciones aritmeticas en variables tipo ", GlobalVariables.type_flag)
            # Estamos trabajando con un valor numerico, guardamos que tipo de operacion es.
            else:
                GlobalVariables.current_operator = token.type
                GlobalVariables.state += 1
        else:
            if token.type != ';':
                print("Error in line", token.lineno, ": Syntax error")
                sys.exit(2)

    # Ya tenemos la operacion, ahora el valor
    elif GlobalVariables.state == 4:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER':
            # 1. Checar si mi variable soporta ese tipo
            if GlobalVariables.checkValue(token.value, GlobalVariables.type_flag):
                # 2. Asignar esa variable
                GlobalVariables.current_variable_value = arithmetic(
                    GlobalVariables.current_variable_value, token.value, GlobalVariables.current_operator)
                GlobalVariables.state -= 1  # Regresamos a esperar otra operacion
            else:
                print('Error in line', token.lineno, ':  Variable type',
                      GlobalVariables.type_flag, 'doesnt support value: ', token.value)
                sys.exit(2)

        # Si nos da un ID
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! : ",
                      GlobalVariables.symbol_table[token.value])
                # 2. Checar si sus tipos son compatibles
                if GlobalVariables.checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.type_flag):
                    # 2. Asignar esa variable
                    GlobalVariables.current_variable_value = arithmetic(
                        GlobalVariables.current_variable_value, GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.current_operator)
                    GlobalVariables.state -= 1  # Regresamos a esperar otra operacion
                else:
                    print('Error in line', token.lineno, ': Variable type', GlobalVariables.type_flag,
                          'doesnt support value: ', GlobalVariables.symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
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
                print('Error in line', token.lineno, ':  Variable type',
                      GlobalVariables.type_flag, 'doesnt support value: ', token.value)
                sys.exit(2)

        # Si nos da un ID
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! : ",
                      GlobalVariables.symbol_table[token.value])
                # 2. Checar si sus tipos son compatibles
                if checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.type_flag):
                    # 2. Asignar esa variable
                    GlobalVariables.current_variable_value = GlobalVariables.symbol_table[
                        token.value]['value']
                    GlobalVariables.state += 1
                else:
                    print('Error in line', token.lineno, ': Variable type', GlobalVariables.type_flag,
                          'doesnt support value: ', GlobalVariables.symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)

    elif GlobalVariables.state == 2:
        # Si el usuario quiere hacer una operacion durante asignacion
        if token.type == 'PLUS' or token.type == 'MINUS' or token.type == 'TIMES' or token.type == 'DIVIDE' or token.type == 'MOD':
            # Si tenemos BOOL o CHAR, tirar error porque no hace sentido hacer operaciones
            if GlobalVariables.type_flag == 'BOOL_TYPE' or GlobalVariables.type_flag == 'CHAR_TYPE':
                print("Error in line", token.lineno,
                      ":  No se pueden hacer operaciones aritmeticas en variables tipo ", GlobalVariables.type_flag)
            # Estamos trabajando con un valor numerico, guardamos que tipo de operacion es.
            else:
                GlobalVariables.current_operator = token.type
                GlobalVariables.state += 1
        else:
            if token.type != ';':
                print("Error in line", token.lineno, ": Syntax error")
                sys.exit(2)

    # Ya tenemos la operacion, ahora el valor
    elif GlobalVariables.state == 3:
        # Si nos da un valor
        if token.type == 'FLOAT' or token.type == 'INTEGER':
            # 1. Checar si mi variable soporta ese tipo
            if checkValue(token.value, GlobalVariables.type_flag):
                # 2. Asignar esa variable
                GlobalVariables.current_variable_value = arithmetic(
                    GlobalVariables.current_variable_value, token.value, GlobalVariables.current_operator)
                GlobalVariables.state -= 1  # Regresamos a esperar otra operacion
            else:
                print('Error in line', token.lineno, ':  Variable type',
                      GlobalVariables.type_flag, 'doesnt support value: ', token.value)
                sys.exit(2)

        # Si nos da un ID
        elif token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! : ",
                      GlobalVariables.symbol_table[token.value])
                # 2. Checar si sus tipos son compatibles
                if checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.type_flag):
                    # 2. Asignar esa variable
                    GlobalVariables.current_variable_value = arithmetic(
                        GlobalVariables.current_variable_value, GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.current_operator)
                    GlobalVariables.state -= 1  # Regresamos a esperar otra operacion
                else:
                    print('Error in line', token.lineno, ': Variable type', GlobalVariables.type_flag,
                          'doesnt support value: ', GlobalVariables.symbol_table[token.value]['value'])
                    sys.exit(2)
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)


def variables(token):
    # If we know we are assigning a variable:
    if token.type == ';':
        if GlobalVariables.assign_variable_flag == True or GlobalVariables.modify_existing_varaible_flag == True:
            assign_variable(token)
            print('Finished!', GlobalVariables.current_variable_ID,
                  GlobalVariables.type_flag, GlobalVariables.current_variable_value)
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

    else:  # We got a new token and don't know what to do with it
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
                GlobalVariables.current_variable_value = GlobalVariables.symbol_table[
                    token.value]['value']

        else:
            print('pass')
