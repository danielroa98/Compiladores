
'''
Antonio Junco de Haas - A01339695
Luis Daniel Roa González - A01021960
Sergio Hernández Castillo - A01025210
Sebastián Gonzalo Vives Faus - A01025211

'''

import sys
import GlobalVariables

# Import methods
import assign_array
import prints
import structure
import variables_doc
#import loopAndConditionalAnalysis


def func_resetFlags():
    GlobalVariables.state = 0
    GlobalVariables.current_variable_ID = ''
    GlobalVariables.type_flag = ''
    GlobalVariables.declare_function_flag = False
    GlobalVariables.function_arg_type = ''
    GlobalVariables.function_args = []
    GlobalVariables.function_tokens = []
    GlobalVariables.run_function_flag = False
    GlobalVariables.function_state = 0

def run_function(token):
    # Si ya inicie, lo mando a este metodo
    if GlobalVariables.run_function_flag == True:
        prepare_function(token)
    
    # Si no, vamos a checar que tipo de token es
    else:
        if token.type == 'ID':
            if GlobalVariables.symbol_table[token.value]['type'] == 'FUNC':
                GlobalVariables.run_function_flag = True
                GlobalVariables.current_variable_ID = token.value
            else:
                print("run_function: pass")
        else:
            print("run_function: pass")

def prepare_function(token):
    # Ya tenemos el tipo de print, ahora esperamos un '('
    if GlobalVariables.function_state == 0:
        # Validacion
        if token.type == '(':
            GlobalVariables.function_state += 1
        else:
            print('Syntax error: Expected a (')
            sys.exit(2)

    elif GlobalVariables.function_state == 1:
        # Validacion
        if token.type == ')':
            GlobalVariables.function_state += 1
        else:
            print('Syntax error: Expected a )')
            sys.exit(2)

    elif GlobalVariables.function_state == 2:
        # Validacion
        if token.type == ';':
            print('Starting funtion...')

            # Here we start executing all tokens inside our function
            for ftoken in GlobalVariables.symbol_table[GlobalVariables.current_variable_ID]['tokens']:
                program_init(ftoken)
            
            print("Finishing fuction!")

            func_resetFlags()

        else:
            print('Syntax error: Expected a ;')
            sys.exit(2)


def program_init(token):
    print(token)
    if GlobalVariables.assign_variable_flag == True or GlobalVariables.assign_array_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.if_flag == True or GlobalVariables.declare_function_flag == True or GlobalVariables.declare_struct_flag == True or GlobalVariables.while_loop_flag == True:
        print('No print statement detected.')
        print('')
    else:
        prints.what_print(token)

    if GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True or GlobalVariables.if_flag == True or GlobalVariables.declare_function_flag == True or GlobalVariables.declare_struct_flag == True or GlobalVariables.while_loop_flag == True:
            print('No variable detected.')
            print('')
    else:
        variables_doc.variables(token)


    if GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True or GlobalVariables.assign_variable_flag == True or GlobalVariables.assign_array_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.declare_function_flag == True or GlobalVariables.declare_struct_flag == True:
        print('No if or while detected.')
        print('')
    else:
        #checkLoop(token)
        print('Checking loop...')

    if GlobalVariables.assign_variable_flag == True or GlobalVariables.assign_array_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.if_flag == True or GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True or GlobalVariables.while_loop_flag == True:
        #if 'FINISH' in token:
        print('No structure detected.')
        print('')
    else:
        structure.define_struct(token)
