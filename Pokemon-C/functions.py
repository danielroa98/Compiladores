import sys
import GlobalVariables


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
            print("pokefunction: pass")

def pokefunction(token):
    # Expecting a vartype
    if GlobalVariables.state == 0:
        # Espero un tipo de variable ("incluyedo SHADOW")
        if token.type == 'VOID' or token.type == 'INT_TYPE' or token.type == 'FLOAT_TYPE':
            GlobalVariables.type_flag = token.type
            GlobalVariables.state += 1
        else:
            print('ERROR: Syntax, expected a VAR_TYPE')
    
    # I want the ID for the function
    elif GlobalVariables.state == 1:
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
            print('Syntax error')
            sys.exit(2)

    # Ya tenemos el tipo de print, ahora esperamos un '('
    elif GlobalVariables.state == 2:
        # Validacion
        if token.type == '(':
            GlobalVariables.state += 1
        else:
            print('Syntax error: Expected a (')
            sys.exit(2)

    # LOOP WARNING: Expecting VAR_TYPE or )
    elif GlobalVariables.state == 3:
         # Validacion
        # Espero un tipo de variable
        if token.type == 'INT_TYPE' or token.type == 'FLOAT_TYPE':
            GlobalVariables.function_arg_type = token.type
            GlobalVariables.state += 1

        elif token.type == ')':
            GlobalVariables.state = 6
        else:
            print('Syntax error: Expected a ) or VAR_TYPE')
            sys.exit(2)
    
    # LOOP WARNING: Expecting an ID
    elif GlobalVariables.state == 4:
        # Validacion
        if token.type == 'ID':
            # Guardar ID y su tipo
                GlobalVariables.function_args.append({
                    'id': token.value,
                    'type':  GlobalVariables.function_arg_type
                    })
                GlobalVariables.state += 1

        else:
            print('Syntax error')
            sys.exit(2)

    # LOOP WARNING: , or )
    elif GlobalVariables.state == 5:
        if token.type == ',':
            GlobalVariables.state = 3

        elif token.type == ')':
            GlobalVariables.state = 6
        else:
            print('Syntax error: Expected a ) or VAR_TYPE')
            sys.exit(2)

    # Finish with ;
    elif GlobalVariables.state == 6:
        if token.type == ';':
            # Guardar fucion
            GlobalVariables.symbol_table[GlobalVariables.current_variable_ID] = {
                'type': GlobalVariables.type_flag,
                'args': GlobalVariables.function_args
            }
            print('Finished! function', GlobalVariables.symbol_table[GlobalVariables.current_variable_ID])
            resetFlags()
            print('finish?')
            

        else:
            print("ERROR: Expecting ;")