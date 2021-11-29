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
                print("ID existe! : ", GlobalVariables.symbol_table[token.value])
                GlobalVariables.var1_type = GlobalVariables.symbol_table[token.value]['type']
                GlobalVariables.var1_value = GlobalVariables.symbol_table[token.value]['value']
                GlobalVariables.if_state_flag += 1
            else:
                print("Error en la línea", token.lineno, ":  La variable ", token.value, ' no está definida.')
                sys.exit(2)
        else:
            print('ERROR: Esperaba el nombre de una variable.')
            sys.exit(2)

    # State case 2: awaiting the logical operation in the if.
    elif GlobalVariables.if_state_flag == 2:
        if token.type == 'EQ' or token.type == 'LE' or token.type == 'GE' or token.type == 'GT' or token.type == 'LT' or token.type == 'NE':
            GlobalVariables.comparacion = token.type
            GlobalVariables.if_state_flag += 1
        else:
            print("Error en la línea", token.lineno, ": Error de sintáxis", token.value)
            sys.exit(2)

    # State case 3: awaiting the second variable to analyze
    elif GlobalVariables.if_state_flag == 3:
        if token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID existe! : ", GlobalVariables.symbol_table[token.value])
                if GlobalVariables.checkValue(GlobalVariables.symbol_table[token.value]['value'], GlobalVariables.var1_type):
                    GlobalVariables.var2_type = GlobalVariables.symbol_table[token.value]['type']
                    GlobalVariables.var2_value = GlobalVariables.symbol_table[token.value]['value']
                    GlobalVariables.if_state_flag += 1
                else:
                    print("ERROR: Las variables no son del mismo tipo")
                    sys.exit(2)
            else:
                print("Error en la línea", token.lineno, ":  La variable ",
                      token.value, ' no está definida.')
                sys.exit(2)
        else:
            print("ERROR: Esperaba el nombre de una variable.")
            sys.exit(2)

    # State case 4: awaiting the second parenthesis in order to validate the logical operation
    elif GlobalVariables.if_state_flag == 4:
        if token.type == ')':
            # print(GlobalVariables.comparacion)

            if GlobalVariables.logicalOperations(GlobalVariables.var1_value, GlobalVariables.var2_value, GlobalVariables.comparacion):
                GlobalVariables.if_state_flag += 1
                GlobalVariables.conditional_op_flag = True
            else:
                GlobalVariables.if_state_flag = 7
        else:
            print("ERROR: Esperaba un )")
            sys.exit(2)

    # State case 5: awaits the openning bracket in order to start reading the contents of the IF.
    elif GlobalVariables.if_state_flag == 5:
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
            program_init(token)

    # State case 7: awaits the closing bracket corresponding to the IF statement
    elif GlobalVariables.if_state_flag == 7:
        if token.type == '}':
            GlobalVariables.if_state_flag += 1
        elif token.type != '}' and GlobalVariables.conditional_op_flag == False:
            print('AVISO: Ignorando el contenido del if.')
        else:
            print('ERROR: esperaba un }')
            sys.exit(2)

    # State case 8: awaiting the declaration of the else or the ;
    elif GlobalVariables.if_state_flag == 8:
        if token.type == 'ELSE' and GlobalVariables.conditional_op_flag == False:
            GlobalVariables.if_state_flag = 5
        elif GlobalVariables.conditional_op_flag == True:
            if token.type == ';':
                resetIfFlags()
        elif token.type == ';' and GlobalVariables.conditional_op_flag == False:
            resetIfFlags()
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
        if token.type == 'ID':
            # 1. Checar si ese ID ya existe en mi tabla de simbolos
            if token.value in GlobalVariables.symbol_table.keys():
                print("ID existe! :",
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
            print("ERROR: Esperaba el nombre de una variable.")
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
        # A ver, que variable / valor estamos esperando
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
                    print("ERROR: Variables no son del mismo tipo.")
            else:
                print("Error en la línea", token.lineno, ": La variable ",
                      token.value, ' no está definida.')
                sys.exit(2)
        else:
            print("ERROR: Esperaba el nombre de una variable.")
            sys.exit(2)

    elif GlobalVariables.while_state == 4:
        if token.type == ')':
            print(GlobalVariables.comparacion)

            if GlobalVariables.logicalOperations(GlobalVariables.var1_value, GlobalVariables.var2_value, GlobalVariables.comparacion):
                GlobalVariables.conditional_op_flag = True
                GlobalVariables.while_state += 1

            else:
                GlobalVariables.conditional_op_flag = False
                GlobalVariables.while_state = 8
        else:
            print("ERROR: Esperaba un )")
            sys.exit(2)

    elif GlobalVariables.while_state == 5:
        if token.type == '{':
            GlobalVariables.while_state += 1
        else:
            print('ERROR: Esperaba un {')
            sys.exit(2)

    elif GlobalVariables.while_state == 6:
        if token.type == '}':

            GlobalVariables.while_list_len = len(GlobalVariables.token_list)

            while GlobalVariables.logicalOperations(GlobalVariables.var1_value, GlobalVariables.var2_value, GlobalVariables.comparacion):
                # print('Current values are:', GlobalVariables.logicalOperations(GlobalVariables.var1_value, GlobalVariables.var2_value, GlobalVariables.comparacion), 'X=', GlobalVariables.var1_value, 'Y=',GlobalVariables.var2_value)
                for x in GlobalVariables.token_list:
                    program_init(x)
            
                GlobalVariables.var1_value = GlobalVariables.symbol_table[GlobalVariables.while_logical_op[0]]['value']
                GlobalVariables.var2_value = GlobalVariables.symbol_table[GlobalVariables.while_logical_op[1]]['value']

            GlobalVariables.while_state+=1
        else:
            GlobalVariables.token_list.append(token)

    elif GlobalVariables.while_state == 7:
        if token.type == ';':
            resetIfFlags()
        else:
            print('ERROR: Falta ;')
            sys.exit(2)

    elif GlobalVariables.while_state == 8:
        if token.type == '}':
            GlobalVariables.while_state = 7
        elif token.type != '}' and GlobalVariables.conditional_op_flag == False:
            print('AVISO: Ignorando el contenido del while.')
        else:
            print('ERROR: esperaba un }')
            sys.exit(2)

# Program INIT
def program_init(token):

    if GlobalVariables.if_new_variable_flag == True or GlobalVariables.if_modify_variable_flag == True or GlobalVariables.if_array_flag == True:
        print('')
    else:
        prints.what_print(token)

    if GlobalVariables.if_print_flag == True or GlobalVariables.if_print_new_line_flag == True:
        print('')
    else:
        variables_doc.variables(token)
