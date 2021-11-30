
'''
Antonio Junco de Haas - A01339695
Luis Daniel Roa González - A01021960
Sergio Hernández Castillo - A01025210
Sebastián Gonzalo Vives Faus - A01025211

'''

import sys
import GlobalVariables

'''
STRUCT ID {
    VAR_TYPE ID;
    VAR_TYPE ID;*
};

- Grammar
          0     1    2           3     4    2           3
STRUCT -> ID -> { -> VAR_TYPE -> ID -> ; -> VAR_TYPE -> ID *...
                  -> } -> ;              -> } -> ;
                     2    5                 2    5
'''

def resetFlags():
    GlobalVariables.state = 0
    GlobalVariables.struct_state = 0
    GlobalVariables.current_variable_ID = ''
    GlobalVariables.type_flag = ''
    GlobalVariables.declare_struct_flag = False
    GlobalVariables.struct_variable_ID = ''
    GlobalVariables.struct_variables = []

def define_struct(token):
    # Si ya inicie, lo mando a este metodo
    if GlobalVariables.declare_struct_flag == True:
        pokemon_struct(token)
    
    # Si no, vamos a checar que tipo de token es
    else:
        if token.type == 'STRUCT':
            GlobalVariables.declare_struct_flag = True 
        else:
            print("")

def pokemon_struct(token):
    # Obtenemos el ID de la estuctura
    if GlobalVariables.struct_state == 0:
        # Validacion
        if token.type == 'ID':
            # Validar que no exista el ID
            if token.value in GlobalVariables.symbol_table.keys():
                print("Error in line",token.lineno,":  Variable ",token.value,' is already defined.')
                sys.exit(2)
            else:
                GlobalVariables.current_variable_ID = token.value
                GlobalVariables.struct_state += 1

        else:
            print('Error in line', token.lineno, ': Syntax error')
            sys.exit(2)

    # Esperamos un {
    elif GlobalVariables.struct_state == 1:
         # Validacion
        if token.type == '{':
            GlobalVariables.struct_state += 1
        else:
            print("Error in line",token.lineno,":  Expected a {")
            sys.exit(2)

    # LOOP WARNING: Esperamos ya sea un VAR_TYPE o }
    elif GlobalVariables.struct_state == 2:
        # Si recibo un }, significa que la declaracio de mi STRUCT termino
        if token.type == '}':
            GlobalVariables.struct_state = 5
        # Espero un tipo de variable
        elif token.type == 'FLOAT_TYPE' or token.type == 'INT_TYPE' or token.type == 'CHAR_TYPE' or token.type == 'BOOL_TYPE':
            GlobalVariables.type_flag = token.type
            GlobalVariables.struct_state = 3
        else:
            print("Error in line",token.lineno,":  Expected a VAR_TYPE or }")
            sys.exit(2)

    # LOOP WARNING: Esperamos el ID de la variable
    elif GlobalVariables.struct_state == 3:
        # Esperamos ID
        if token.type == 'ID':
            GlobalVariables.struct_variable_ID = token.value
            GlobalVariables.struct_state = 4
        else:
            print("Error in line",token.lineno,":  Expected an ID")
            sys.exit(2)
    
    # LOOP WARNING: Esperamos ; como fin de la variable
    elif GlobalVariables.struct_state == 4:
         # Validacion
        if token.type == ';':
            GlobalVariables.struct_variables.append({
                'type': GlobalVariables.type_flag,
                'ID': GlobalVariables.struct_variable_ID
            })
            GlobalVariables.struct_state = 2
        else:
            print("Error in line",token.lineno,":  Expected a ;")
            sys.exit(2)

    # Se termino el STRUCT
    elif GlobalVariables.struct_state == 5:
         # Validacion
        if token.type == ';':
            GlobalVariables.symbol_table[GlobalVariables.current_variable_ID] = {
                'variables': GlobalVariables.struct_variables
            }
            print('Finished! Struct: ',GlobalVariables.current_variable_ID, GlobalVariables.symbol_table[GlobalVariables.current_variable_ID])
            resetFlags()
        else:
            print("Error in line",token.lineno,":  Expected a ;")
            sys.exit(2)
