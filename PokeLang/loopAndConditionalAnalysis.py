
'''
Antonio Junco de Haas - A01339695
Luis Daniel Roa González - A01021960
Sergio Hernández Castillo - A01025210
Sebastián Gonzalo Vives Faus - A01025211

'''

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
    GlobalVariables.if_state_flag = 0
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
    GlobalVariables.conditional_op_flag = False


def resetWhileFlags():
    GlobalVariables.var1_type = ''
    GlobalVariables.var1_value = ''
    GlobalVariables.var2_type = ''
    GlobalVariables.var2_value = ''
    GlobalVariables.comparacion = ''
    # program_init
    GlobalVariables.if_print_flag = False
    GlobalVariables.if_print_new_line_flag = False
    GlobalVariables.if_new_variable_flag = False
    GlobalVariables.if_modify_variable_flag = False
    GlobalVariables.if_array_flag = False

    GlobalVariables.while_loop_flag = False
    GlobalVariables.while_logical_op = []
    GlobalVariables.token_list = []
    GlobalVariables.while_state = 0
    GlobalVariables.conditional_op_flag = False


def checkIfandElse(token):
    print('Checking IF')
    # State case 0: waiting for '('
    if GlobalVariables.if_state_flag == 0:
        if token.type == '(':
            GlobalVariables.if_state_flag += 1
        else:
            print('ERROR: esperaba un (')
            sys.exit(2)

    # State case 1: waiting for the first variable to analyze
    elif GlobalVariables.if_state_flag == 1:
        # Await to analyze the variable/value received
        if token.type == 'ID':
            # 1. If the value received is in the symbol table
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! : ",
                      GlobalVariables.symbol_table[token.value])
                GlobalVariables.var1_type = GlobalVariables.symbol_table[token.value]['type']
                GlobalVariables.var1_value = GlobalVariables.symbol_table[token.value]['value']
                GlobalVariables.if_state_flag += 1
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)
        else:
            print('ERROR: esperaba un valor o una variable.')
            sys.exit(2)

    # State case 2: awaiting the logical operation in the if.
    elif GlobalVariables.if_state_flag == 2:
        print('Second state\n')
        if token.type == 'EQ' or token.type == 'LE' or token.type == 'GE' or token.type == 'GT' or token.type == 'LT' or token.type == 'NE':
            GlobalVariables.comparacion = token.type
            GlobalVariables.if_state_flag += 1
        else:
            print("IF Error in line", token.lineno,
                  ": Syntax error", token.value)
            sys.exit(2)

    # State case 3: awaiting the second variable to analyze
    elif GlobalVariables.if_state_flag == 3:
        if token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("IF ID exists! : ",
                      GlobalVariables.symbol_table[token.value])
                if GlobalVariables.checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.var1_type):
                    GlobalVariables.var2_type = GlobalVariables.symbol_table[token.value]['type']
                    GlobalVariables.var2_value = GlobalVariables.symbol_table[token.value]['value']
                    GlobalVariables.if_state_flag += 1
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
    elif GlobalVariables.if_state_flag == 4:
        if token.type == ')':
            # print(GlobalVariables.comparacion)

            if GlobalVariables.logicalOperations(GlobalVariables.var1_value, GlobalVariables.var2_value, GlobalVariables.comparacion):
                # print('Si cumple\nState 4')
                print('\nLogical operation is true')
                GlobalVariables.if_state_flag += 1
                GlobalVariables.conditional_op_flag = True
            else:
                print('\nLogical operation is false')
                print('Checking the existance of an ELSE')
                GlobalVariables.if_state_flag = 7
        else:
            print("ERROR: Esperaba un )")
            sys.exit(2)

    # State case 5: awaits the openning bracket in order to start reading the contents of the IF.
    elif GlobalVariables.if_state_flag == 5:
        print('\nIn state 5', token)
        if token.type == '{':
            GlobalVariables.if_state_flag += 1
        else:
            print('ERROR: esperaba un {')
            sys.exit(2)

    # State case 6: starts reading the operations inside the if cycle while it awaits a closing bracket
    elif GlobalVariables.if_state_flag == 6:

        if token.type == '}':
            GlobalVariables.if_state_flag = 8
        else:
            print('Reading variables')
            program_init(token)

    # State case 7: awaits the closing bracket corresponding to the IF statement
    elif GlobalVariables.if_state_flag == 7:
        if token.type == '}':
            GlobalVariables.if_state_flag += 1
        elif token.type != '}' and GlobalVariables.conditional_op_flag == False:
            print('Ignoring content')
        else:
            print('ERROR: esperaba un }')
            sys.exit(2)

    # State case 8: awaiting the declaration of the else or the ;
    elif GlobalVariables.if_state_flag == 8:
        if token.type == 'ELSE' and GlobalVariables.conditional_op_flag == False:
            print('Detected an else')
            GlobalVariables.if_state_flag = 5
        elif GlobalVariables.conditional_op_flag == True:
            print('Ignoring ELSE')
            if token.type == ';':
                print('Closing statement')
                resetIfFlags()
                print('Resetted flags')
        elif token.type == ';' and GlobalVariables.conditional_op_flag == False:
            print('If was false\nNo else detected')
            resetIfFlags()
            print('Resetted flags')
        else:
            print('ERROR: no hay seguimiento en la operación. (Falta un ELSE o un ;)')
            sys.exit(2)


def whileAnalysis(token):

    # State 0: start logical operation in the WHILE loop
    if GlobalVariables.while_state == 0:
        # print('State 0 received', token)
        if token.type == '(':
            GlobalVariables.while_state += 1
        else:
            print('ERROR: Esperaba un (')
            sys.exit(2)

    # State 1: received first variable in the logical operation
    elif GlobalVariables.while_state == 1:
        print('State 1 received', token)
        if token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! :",
                      GlobalVariables.symbol_table[token.value])
                GlobalVariables.var1_type = GlobalVariables.symbol_table[token.value]['type']
                GlobalVariables.var1_value = GlobalVariables.symbol_table[token.value]['value']

                GlobalVariables.while_logical_op.append(token.value)
                # print('\nGV.WV',GlobalVariables.while_vars,'\n')
                GlobalVariables.while_state += 1
            else:
                print("Error en la línea", token.lineno, ":  Variable ",
                      token.value, ' no está definida.')
                sys.exit(2)
        else:
            print("ERROR: Esperaba un valor/variable primer lugar")
            sys.exit(2)

    elif GlobalVariables.while_state == 2:
        if token.type == 'EQ' or token.type == 'LE' or token.type == 'GE' or token.type == 'GT' or token.type == 'LT' or token.type == 'NE':
            GlobalVariables.comparacion = token.type
            GlobalVariables.while_state += 1
        elif token.type == ')':
            GlobalVariables.while_state = 5
        else:
            print("Error en la línea", token.lineno,
                  ": Error de sintáxis", token.value)
            sys.exit(2)

    elif GlobalVariables.while_state == 3:
        # A ver, que variable / valor estamos esperando ?
        print('State 3 received', token)
        if token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID exists! :",
                      GlobalVariables.symbol_table[token.value])
                if GlobalVariables.checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.var1_type):
                    GlobalVariables.var2_type = GlobalVariables.symbol_table[token.value]['type']
                    GlobalVariables.var2_value = GlobalVariables.symbol_table[token.value]['value']

                    GlobalVariables.while_logical_op.append(token.value)
                    GlobalVariables.while_state += 1
                    print('\nToken values are', GlobalVariables.while_logical_op,
                          'and the operation is', GlobalVariables.comparacion)
                else:
                    print("ERROR: No son del mismo tipo")
            else:
                print("Error in line", token.lineno, ":  Variable ",
                      token.value, ' is not defined.')
                sys.exit(2)
        else:
            print("ERROR: Esperaba un valor/variable segundo lugar")
            sys.exit(2)

    elif GlobalVariables.while_state == 4:
        if token.type == ')':
            print(GlobalVariables.comparacion)

            if GlobalVariables.logicalOperations(GlobalVariables.var1_value, GlobalVariables.var2_value, GlobalVariables.comparacion):
                GlobalVariables.conditional_op_flag = True
                print('\nLogical operation is true')
                GlobalVariables.while_state += 1

            else:
                print('\nLogical operation is false')
                print('Exiting while')
                GlobalVariables.conditional_op_flag = False
                GlobalVariables.while_state = 8
        else:
            print("ERROR: Esperaba un )")
            sys.exit(2)

    elif GlobalVariables.while_state == 5:
        if token.type == '{':
            print('Started to read the operations inside the WHILE')
            GlobalVariables.while_state += 1
        else:
            print('ERROR: Esperaba un {')
            sys.exit(2)

    elif GlobalVariables.while_state == 6:
        if token.type == '}':

            GlobalVariables.while_list_len = len(GlobalVariables.token_list)


            while GlobalVariables.logicalOperations(GlobalVariables.var1_value, GlobalVariables.var2_value, GlobalVariables.comparacion):
                print('Current values are:', GlobalVariables.logicalOperations(GlobalVariables.var1_value, GlobalVariables.var2_value, GlobalVariables.comparacion), 'X=', GlobalVariables.var1_value, 'Y=',GlobalVariables.var2_value)
                for x in GlobalVariables.token_list:
                    #Flag = true; si la flag es true ignorar while, no puedes entrar, porque estas ejecutando
                    program_init(x)
                    print('Inside for iteration')
                
            
                GlobalVariables.var1_value = GlobalVariables.symbol_table[GlobalVariables.while_logical_op[0]]['value']
                GlobalVariables.var2_value = GlobalVariables.symbol_table[GlobalVariables.while_logical_op[1]]['value']

                print('Finished for iteration')
                # GlobalVariables.while_state += 1

            GlobalVariables.while_state+=1
        else:
            GlobalVariables.token_list.append(token)

    elif GlobalVariables.while_state == 7:
        if token.type == ';':
            print('Done processing while')
            resetIfFlags()
        else:
            print('ERROR: missing ;')
            sys.exit(2)

    elif GlobalVariables.while_state == 8:
        if token.type == '}':
            GlobalVariables.while_state = 7
        elif token.type != '}' and GlobalVariables.conditional_op_flag == False:
            print('Ignoring content')
        else:
            print('ERROR: esperaba un }')
            sys.exit(2)

# Program INIT
def program_init(token):

    print('Banderita de mi IF PRINT FLAG', GlobalVariables.if_print_flag)

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
