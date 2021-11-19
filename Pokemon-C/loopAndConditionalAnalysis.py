import GlobalVariables
import sys

def resetIfFlags():
    GlobalVariables.if_flag = False
    GlobalVariables.state = False
    GlobalVariables.var1_type = ''
    GlobalVariables.var1_value = ''
    GlobalVariables.var2_type = ''
    GlobalVariables.var2_value = ''
    GlobalVariables.comparacion = ''

def checkConditional(token):

    # 0. Esperamos un parentesis izquierdo
    if GlobalVariables.state == 0:
        if token.type == '(':
            GlobalVariables.state += 1
        else:
            print("ERROR: Esperaba un (")

    # 1. Espero una variable
    elif GlobalVariables.state == 1:
        # A ver, que variable / valor estamos esperando ?
        if token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! : ", GlobalVariables.symbol_table[token.value])
                GlobalVariables.var1_type = GlobalVariables.symbol_table[token.value]['type']
                GlobalVariables.var1_value = GlobalVariables.symbol_table[token.value]['value']
                GlobalVariables.state += 1
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)
        else:
            print("ERROR: Esperaba un valor / variable primer lugar")
            sys.exit(2)

    # 2. Espero una operacion logica
    elif GlobalVariables.state == 2:
        if token.type == 'EQ' or token.type == 'LE' or token.type == 'GE' or token.type == 'GT' or token.type == 'LT' or token.type == 'NE':
            GlobalVariables.comparacion = token.type
            GlobalVariables.state += 1
        elif token.type == ')':
            GlobalVariables.state = 5
        else:
            print("Error in line", token.lineno, ": Syntax error", token.value)
            sys.exit(2)

    # 3. Espero mi segunda variable
    elif GlobalVariables.state == 3:
     # A ver, que variable / valor estamos esperando ?
        if token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! : ", GlobalVariables.symbol_table[token.value])
                if GlobalVariables.checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.var1_type):
                    GlobalVariables.var2_type = GlobalVariables.symbol_table[token.value]['type']
                    GlobalVariables.var2_value = GlobalVariables.symbol_table[token.value]['value']
                    GlobalVariables.state += 1
                else:
                    print("ERROR: No son del mismo tipo, pelas")
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)
        else:
            print("ERROR: Esperaba un valor/variable segundo lugar")
            sys.exit(2)

    # Ahora espero cerrar la comparacion
    elif GlobalVariables.state == 4:
        if token.type == ')':
            print(GlobalVariables.comparacion)

            if GlobalVariables.logicalOperations(GlobalVariables.var1_value, GlobalVariables.var2_value, GlobalVariables.comparacion):
                print('Si cumple\nState 4')
            else:
                print('Chole con tus quejas')
                GlobalVariables.state = 5
        else:
            print("ERROR: Esperaba un )")
            sys.exit(2)

    # Hacer la comparacion, ver si es valida, que te regresa y guardarla en diccionario (poner si vas a empezar if o while)
    # Resetear todas las banderas declaradas
    # {'IF': var1 {TYPE: 'INT_TYPE', 'value': 100}, 'var2': {'type': 'INT_TYPE', 'value': 110}, OPERATION}

    # me la pela todo el if, pero al else se a chupo
    elif GlobalVariables.state == 5:
        if token.type == 'ELSE':
            print('wakey wakey is time fo school')
            '''
            correrElse(token):

            state 0:
                detectar {
            
            state 1:
                si detecta }, reset flags, se acaba el if
                si no:
                    varaibles()
                    prints()
                    ...
            '''
        else:
            print('pass...')

    # Si paso, pero el else me la pela
    elif GlobalVariables.state == 6:
        '''
            state 0:
                detectar {
            state 1:
                si detecta }, mandar a state 7
                si no:
                    varaibles()
                    prints()
                    ...
        '''

    # Si paso, pero el else me la pela
    elif GlobalVariables.state == 7:
        '''
            if token.type == }
                reset flags
            else:
                print(pass...)
            
        '''
