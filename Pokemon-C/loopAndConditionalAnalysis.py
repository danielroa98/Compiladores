import GlobalVariables
import sys

# Import methods
import assign_array
import prints
import structure
import variables_doc

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
    GlobalVariables.if_print_flag = False
    GlobalVariables.if_print_new_line_flag = False
    GlobalVariables.if_new_variable_flag = False
    GlobalVariables.if_modify_variable_flag = False
    GlobalVariables.if_array_flag = False

def checkIfandElse(token):
    
    print(' SOY EL STATE: ', GlobalVariables.state)
    
    """ 
    Function checkIfandElse
    
    Receives:
        token: value of the current token being analysed.
    Returns:
        Nothing, updates values regarding the IF and WHILE operators.
    """
    # State case 0: waiting for '('
    if GlobalVariables.state == 0:
        if token.type == '(':
            GlobalVariables.state += 1
        else:
            print('ERROR: esperaba un (')
            sys.exit(2)
    
    # State case 1: waiting for the first variable to analyze
    elif GlobalVariables.state == 1:
        # Await to analyze the variable/value received
        if token.type == 'ID':
            #1. If the value received is in the symbol table
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
            print('ERROR: esperaba un valor o una variable.')
            sys.exit(2)
    
    #State case 2: awaiting the logical operation in the if.
    elif GlobalVariables.state == 2:
        print('Second state\n')
        if token.type == 'EQ' or token.type == 'LE' or token.type == 'GE' or token.type == 'GT' or token.type == 'LT' or token.type == 'NE':
            GlobalVariables.comparacion = token.type
            GlobalVariables.state += 1
        else:
            print("IF Error in line", token.lineno, ": Syntax error", token.value)
            sys.exit(2)

    #State case 3: awaiting the second variable to analyze
    elif GlobalVariables.state == 3:
        if token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("IF ID exists! : ",
                      GlobalVariables.symbol_table[token.value])
                if GlobalVariables.checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.var1_type):
                    GlobalVariables.var2_type = GlobalVariables.symbol_table[token.value]['type']
                    GlobalVariables.var2_value = GlobalVariables.symbol_table[token.value]['value']
                    GlobalVariables.state += 1
                else:
                    print("ERROR: Las variables no son del mismo tipo")
                    sys.exit(2)
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)
        else:
            print("ERROR: Esperaba un valor/variable en el segundo lugar")
            sys.exit(2)
    
    # State case 4: awaiting the second parenthesis in order to validate the logical operation
    elif GlobalVariables.state == 4:
        if token.type == ')':
            # print(GlobalVariables.comparacion)

            if GlobalVariables.logicalOperations(GlobalVariables.var1_value, GlobalVariables.var2_value, GlobalVariables.comparacion):
                # print('Si cumple\nState 4')
                print('\nLogical operation is true')
                GlobalVariables.state += 1
            else:
                print('\nLogical operation is false')
                print('Checking the existance of an ELSE')
                GlobalVariables.state = 8
        else:
            print("ERROR: Esperaba un )")
            sys.exit(2)

    # State case 5: awaits the openning bracket in order to start reading the contents of the IF.
    elif GlobalVariables.state == 5:
        print('\nIn state 5', token)
        if token.type == '{':
            GlobalVariables.state += 1
        else:
            print('ERROR: esperaba un {')
            sys.exit(2)

    # State case 6: starts reading the operations inside the if cycle while it awaits a closing bracket
    elif GlobalVariables.state == 6:
        
        if token.type == '}':
            GlobalVariables.state = 8
        else:
            print('Reading variables')
            program_init(token)
            #print('->',token)
        """ if token.type == '}':
            GlobalVariables.state += 1
        else: 
        # TODO: pedir ayuda para implementar las funciones necesarias
        print('Reading variables')
        #program_init(token)
        print('->',token)
        # Might implement the same for cycle located in runFunction.prepare_function line 63
        GlobalVariables.state += 1
        """
    
    # State case 7: awaits the closing bracket corresponding to the IF statement 
    elif GlobalVariables.state == 7:
        print('Token', token)
        if token.type == '}':
            GlobalVariables.state += 1
        else:
            print('ERROR: esperaba un }')
            sys.exit(2)
    
    # State case 8: awaiting the declaration of the else or the ;
    elif GlobalVariables.state == 8:
        print('Current state flag is', GlobalVariables.state)
        if token.type == 'ELSE':
            print('Detected an else')
            GlobalVariables.state = 5
        elif token.type == ';':
            print('Closing statement')
            resetIfFlags()


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
                GlobalVariables.state += 1
            else:
                print('\nEvaluating inside the WHILE\n')
    

# Program INIT
def program_init(token):

    print('Banderita de mi IF PRINT FLAG',GlobalVariables.if_print_flag)

    if GlobalVariables.if_new_variable_flag == True or GlobalVariables.if_modify_variable_flag == True or GlobalVariables.if_array_flag == True:
        print('')
    else:
        print('Voy a entrar a mi print')
        prints.what_print(token)
        print('Sali de mi print')

    if GlobalVariables.if_print_flag == True or GlobalVariables.if_print_new_line_flag == True:
        print('')
    else:
        print('Voy a entrar a mi variablie')
        variables_doc.variables(token)
        print('Sali de mi variablie')
