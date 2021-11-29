import sys
import GlobalVariables

def resetFlags():
    GlobalVariables.state = 0
    GlobalVariables.current_variable_ID = ''
    GlobalVariables.type_flag = ''
    GlobalVariables.print_in_line_flag = False
    GlobalVariables.print_in_newline_flag = False
    GlobalVariables.if_print_flag = False
    GlobalVariables.if_print_new_line_flag = False

# 1. Definir que tipo de print viene
def what_print(token):    
    # Si ya inicie, lo mando a este metodo
    if GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True or GlobalVariables.if_print_flag == True or GlobalVariables.if_print_new_line_flag == True:
        pokeprint(token)
    
    # Si no, vamos a checar que tipo de token es
    else:
        if token.type == 'PRINT_IN_LINE':

            # Si estamos dentro del if...
            if GlobalVariables.if_flag == True:
                GlobalVariables.if_print_flag = True
                GlobalVariables.type_flag = token.type
            else:
                GlobalVariables.type_flag = token.type
                GlobalVariables.print_in_line_flag = True

        elif token.type == 'PRINT_IN_NEW_LINE':

            if GlobalVariables.if_flag == True:
                GlobalVariables.if_print_new_line_flag = True
                GlobalVariables.type_flag = token.type
            else:
                GlobalVariables.type_flag = token.type
                GlobalVariables.print_in_newline_flag = True
        else:
            print("pokeprint: pass")


# Funcion
def pokeprint(token):
    # Ya tenemos el tipo de print, ahora esperamos un '('
    if GlobalVariables.state == 0:
         # Validacion
        if token.type == '(':
            GlobalVariables.state += 1
        else:
            print('Syntax error: Expected a (')
            sys.exit(2)

    # Ahora esperamos una variable para imprimir
    elif GlobalVariables.state == 1:
        # 1. Queremos el ID 
        if token.type == 'ID':

            # 2. Verificar que variable existe en tabla de simbolos
            if GlobalVariables.checkIfVariableIsDefined(token):
                # 3. Ya tenemos la variable, la guardamos
                GlobalVariables.current_variable_ID = token.value
                GlobalVariables.state += 1

        else:
            print("ERROR: Expected a variable")
            sys.exit(2)
    
    # Ahora esperamos un ')'
    elif GlobalVariables.state == 2:
        # Validacion
        if token.type == ')':
            GlobalVariables.state += 1
        else:
            print('Syntax error: Expected a )')
            sys.exit(2)
    
    # Ahora esperamos un ';'
    elif GlobalVariables.state == 3:
        print('Checking for ;')
        # Validacion
        if token.type == ';':
            if GlobalVariables.print_in_line_flag == True:
                resetFlags()

            elif GlobalVariables.print_in_newline_flag == True:
                print('\nJKFHGJKSDFHGJKLSD',GlobalVariables.symbol_table[GlobalVariables.current_variable_ID]['value'])
                resetFlags()

        else:
            print('Syntax error: Expected a ;')
            sys.exit(2)


