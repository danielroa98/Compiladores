import GlobalVariables
import sys

def resetIfFlags():
    GlobalVariables.if_flag = False
    GlobalVariables.while_loop_flag = False
    GlobalVariables.state = 0
    GlobalVariables.inner_operations_state = 0
    GlobalVariables.var1_type = ''
    GlobalVariables.var1_value = ''
    GlobalVariables.var2_type = ''
    GlobalVariables.var2_value = ''
    GlobalVariables.comparacion = ''

def checkConditional(token):
    """ 
    Function checkConditional
    
    Receives:
        token: value of the current token being analysed.
    Returns:
        Nothing, updates values regarding the IF and WHILE operators.
     """
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
                print("IF Error in line", token.lineno, ":  Variable ",
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
            print("IF Error in line", token.lineno, ": Syntax error", token.value)
            sys.exit(2)

    # 3. Espero mi segunda variable
    elif GlobalVariables.state == 3:
     # A ver, que variable / valor estamos esperando ?
        if token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("IF ID exists! : ", GlobalVariables.symbol_table[token.value])
                if GlobalVariables.checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.var1_type):
                    GlobalVariables.var2_type = GlobalVariables.symbol_table[token.value]['type']
                    GlobalVariables.var2_value = GlobalVariables.symbol_table[token.value]['value']
                    GlobalVariables.state += 1
                else:
                    print("ERROR: No son del mismo tipo, pelas")
            else:
                print("WHILE Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)
        else:
            print("ERROR: Esperaba un valor/variable segundo lugar")
            sys.exit(2)

    # Ahora espero cerrar la declaracion dentro del parentesis
    elif GlobalVariables.state == 4:
        if token.type == ')':
            print(GlobalVariables.comparacion)

            if GlobalVariables.logicalOperations(GlobalVariables.var1_value, GlobalVariables.var2_value, GlobalVariables.comparacion):
                # print('Si cumple\nState 4')
                print('\nLogical operation is true')
                GlobalVariables.state = 6
            else:
                print('\nLogical operation is false')
                print('Checking the existance of an ELSE')
                GlobalVariables.state = 5
        else:
            print("ERROR: Esperaba un )")
            sys.exit(2)

    # Hacer la comparacion, ver si es valida, que te regresa y guardarla en diccionario (poner si vas a empezar if o while)
    # Resetear todas las banderas declaradas
    # {'IF': var1 {TYPE: 'INT_TYPE', 'value': 100}, 'var2': {'type': 'INT_TYPE', 'value': 110}, OPERATION}

    #The logical operation declared in the if doesn't work, enters the else
    elif GlobalVariables.state == 5:
        # print('\nCurrent state of the operations flag is', GlobalVariables.inner_operations_state)
        if token.type == 'ELSE':
            print("Logical operation in the IF didn't work, starting the ELSE")
            GlobalVariables.inner_operations_state += 1
        elif GlobalVariables.inner_operations_state == 1:
            if token.type == '{':
                print('Starting to check inside the ELSE')
                GlobalVariables.inner_operations_state += 1
            else:
                print('ERROR: falta declarar un {')
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
        elif GlobalVariables.inner_operations_state == 2:
            print('\nStarting to evaluate the ELSE\n')
            if token.type == '}':
                resetIfFlags()
            else:
                print('\nEvaluating values inside the ELSE\n')
        else:
            print('Finishing evaluation inside the ELSE\n')

    #It entered the IF operation correctly, therefore it ignores the ELSE statement
    elif GlobalVariables.state == 6:
        if token.type == '{':
            GlobalVariables.state += 1
        else:
            print('ERROR: Esperaba un {')
            sys.exit(2)
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

    #Si paso, ahora va a leer las operaciones dentro del loop o if
    elif GlobalVariables.state == 7:
        if token.type == '}':
            print('\nReseting flags\n')
            resetIfFlags()
        else:
            print('\nEvaluating values in the IF cycle\n')
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


    # Si paso, pero el else me la pela
    elif GlobalVariables.state == 9:
        '''
            if token.type == }
                reset flags
            else:
                print(pass...)
            
        '''

def whileAnalysis(token):
    if GlobalVariables.state == 0:
        print('State 0 received', token)
        if token.type == '(':
            GlobalVariables.state += 1
            print('Current value of state flag', GlobalVariables.state)
        else:
            print('ERROR: Esperaba un (')
            sys.exit(2)

    elif GlobalVariables.state == 1:
        print('State 1 received', token)
        if token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("WHILE ID exists! : ",
                      GlobalVariables.symbol_table[token.value])
                GlobalVariables.var1_type = GlobalVariables.symbol_table[token.value]['type']
                GlobalVariables.var1_value = GlobalVariables.symbol_table[token.value]['value']
                GlobalVariables.state += 1
            else:
                print("Error en la línea", token.lineno, ":  Variable ",
                      token.value, ' no está definida.')
                sys.exit(2)
        else:
            print("ERROR: Esperaba un valor/variable primer lugar")
            sys.exit(2)
    
    elif GlobalVariables.state == 2:
        if token.type == 'EQ' or token.type == 'LE' or token.type == 'GE' or token.type == 'GT' or token.type == 'LT' or token.type == 'NE':
            GlobalVariables.comparacion = token.type
            GlobalVariables.state += 1
        elif token.type == ')':
            GlobalVariables.state = 5
        else:
            print("Error en la línea", token.lineno, ": Error de sintáxis", token.value)
            sys.exit(2)

    elif GlobalVariables.state == 3:
        # A ver, que variable / valor estamos esperando ?
        print('State 3 received', token)
        if token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("WHILE ID exists! : ",
                      GlobalVariables.symbol_table[token.value])
                if GlobalVariables.checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.var1_type):
                    GlobalVariables.var2_type = GlobalVariables.symbol_table[token.value]['type']
                    GlobalVariables.var2_value = GlobalVariables.symbol_table[token.value]['value']
                    GlobalVariables.state += 1
                else:
                    print("ERROR: No son del mismo tipo, pelas")
            else:
                print("WHILE Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)
        else:
            print("ERROR: Esperaba un valor/variable segundo lugar")
            sys.exit(2)

    elif GlobalVariables.state == 4:
        if token.type == ')':
            print(GlobalVariables.comparacion)

            if GlobalVariables.logicalOperations(GlobalVariables.var1_value, GlobalVariables.var2_value, GlobalVariables.comparacion):
                # print('Si cumple\nState 4')
                # Since the operation is true, the state will become 5 and it will start reading the contents of the WHILE.
                print('\nLogical operation is true')
                GlobalVariables.state += 1
                
            else:
                print('\nLogical operation is false')
                print('Exiting while')
                GlobalVariables.state = 6
        else:
            print("ERROR: Esperaba un )")
            sys.exit(2)
    
    elif GlobalVariables.state == 5:
        if GlobalVariables.inner_operations_state == 0:
            if token.type == '{':
                print('Started to read the operations inside the WHILE')
                GlobalVariables.inner_operations_state += 1
                print('Flag inner state status:',
                    GlobalVariables.inner_operations_state)
            else:
                print('ERROR: Esperaba un {')
                sys.exit(2)

        if GlobalVariables.inner_operations_state == 1:
            print('Started to processing the operations')
            GlobalVariables.inner_operations_state += 1
        
        elif GlobalVariables.inner_operations_state == 2:
            if token.type == '}':
                resetIfFlags()
            else:
                print('\nEvaluating inside the WHILE\n')
    
