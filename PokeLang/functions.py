'''
Antonio Junco de Haas - A01339695
Luis Daniel Roa González - A01021960
Sergio Hernández Castillo - A01025210
Sebastián Gonzalo Vives Faus - A01025211

'''
import sys
import GlobalVariables



'''
Grammar

FUNC -> ID -> ( -> VAR_TYPE -> ID -> , ...
                -> ) -> {         -> ) -> { -> Save Token
                                            -> } -> ;

'''


def resetFlags():
    GlobalVariables.state = 0
    GlobalVariables.current_variable_ID = ''
    GlobalVariables.type_flag = ''
    GlobalVariables.declare_function_flag = False
    GlobalVariables.function_arg_type = ''
    GlobalVariables.function_args = []

def define_function(token):
    # Si ya inicie, lo mando a este metodo
    if GlobalVariables.declare_function_flag == True:
        pokefunction(token)
    
    # Si no, vamos a checar que tipo de token es
    else:
        if token.type == 'FUNC':
            GlobalVariables.declare_function_flag= True 
        else:
            print("")

def pokefunction(token):
    
    # I want the ID for the function
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
            print('Error in line', token.lineno, ': Syntax error')
            sys.exit(2)

    # Ya tenemos el tipo de print, ahora esperamos un '('
    elif GlobalVariables.state == 1:
        # Validacion
        if token.type == '(':
            GlobalVariables.state += 1
        else:
            print('Error in line', token.lineno, ': Syntax error: Expected a (')
            sys.exit(2)

    # LOOP WARNING: Expecting VAR_TYPE or )
    elif GlobalVariables.state == 2:
         # Validacion
        # Espero un tipo de variable
        if token.type == 'FLOAT' or token.type == 'INTEGER' or token.type == 'CHAR' or token.type == 'BOOL':
            GlobalVariables.function_arg_type = token.type
            GlobalVariables.state += 1

        elif token.type == ')':
            GlobalVariables.state = 6
        else:
            print('Error in line', token.lineno, ': Syntax error: Expected a ) or VAR_TYPE')
            sys.exit(2)
    
    # LOOP WARNING: Expecting an ID
    elif GlobalVariables.state == 3:
        # Validacion
        if token.type == 'ID':
            # Guardar ID y su tipo
                GlobalVariables.function_args.append({
                    'id': token.value,
                    'type':  GlobalVariables.function_arg_type
                    })
                GlobalVariables.state += 1

        else:
            print('Error in line', token.lineno, ': Syntax error')
            sys.exit(2)

    # LOOP WARNING: , or )
    elif GlobalVariables.state == 4:
        if token.type == ',':
            GlobalVariables.state = 2

        elif token.type == ')':
            GlobalVariables.state = 5
        else:
            print('Error in line', token.lineno, ': Syntax error: Expected a ) or VAR_TYPE')
            sys.exit(2)

    elif GlobalVariables.state == 5:
        if token.type == '{':
            GlobalVariables.state = 6
        else:
            print('Error in line', token.lineno, ': Expecting ;')

    elif GlobalVariables.state == 6:
        if token.type == '}':
            GlobalVariables.state = 7
        else:
            GlobalVariables.function_tokens.append(token)

    elif GlobalVariables.state == 7:
        if token.type == ';':
            # Guardar fucion
            GlobalVariables.symbol_table[GlobalVariables.current_variable_ID] = {
                'type': 'FUNC',
                'args': GlobalVariables.function_args,
                'tokens': GlobalVariables.function_tokens
            }
            print('Finished! ',GlobalVariables.current_variable_ID, GlobalVariables.symbol_table[GlobalVariables.current_variable_ID])
            resetFlags()

        else:
            print('Error in line', token.lineno, ': Expecting ;')