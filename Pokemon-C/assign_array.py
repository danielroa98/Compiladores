import sys
import GlobalVariables

def resetFlags():
    GlobalVariables.state = 0
    GlobalVariables.current_variable_ID = ''
    GlobalVariables.array_size = ''
    GlobalVariables.type_flag = ''
    GlobalVariables.assign_array_flag = False

# Asignar un arreglo
def assign_array_variable(token):
    # Espero un ID del arreglo
    if GlobalVariables.state == 0:
        # Validacion
        if token.type == 'ID':
            # Validar que no exista el ID
            if token.value in GlobalVariables.symbol_table.keys():
                print("Error en la línea",token.lineno,":  La variable ",token.value,' ya está definida.')
                sys.exit(2)
            else:
                GlobalVariables.current_variable_ID = token.value
                GlobalVariables.state += 1

        else:
            print('Error de sintáxis')
            sys.exit(2)
    
    # Espero un '='
    elif GlobalVariables.state == 1:
        # Validacion
        if token.type == 'ASSIGN':
            GlobalVariables.state += 1
        else:
            print('Error de sintáxis: Esperaba un =')
            sys.exit(2)
    
    # Espero un '['
    elif GlobalVariables.state == 2:
        # Validacion
        if token.type == '[':
            GlobalVariables.state += 1
        else:
            print('Error de sintáxis: Esperanba un [')
            sys.exit(2)

    # Espero un valor
    elif GlobalVariables.state == 3:
        if token.type == 'FLOAT' or token.type == 'INTEGER' or token.type == 'CHAR' or token.type == 'BOOL':
            GlobalVariables.array_values.append(token.value)
            GlobalVariables.type_flag = token.type # Vamos a comparar el resto de los valores
            GlobalVariables.state += 1

        elif token.type == ']':
            GlobalVariables.state = 6

        else:
            print("ERROR: Esperaba un valor")
            sys.exit(2)

    # LOOP WARNING: Espero un ',' o ']'
    elif GlobalVariables.state == 4:
        # Validacion
        if token.type == ',':
            GlobalVariables.state += 1
        elif token.type == ']':
            GlobalVariables.state = 6
        else:
            print("ERROR: Esperaba una ,")
            sys.exit(2)

    # LOOP WARNING: Espero un valor
    elif GlobalVariables.state == 5:
        if token.type == 'FLOAT' or token.type == 'INTEGER' or token.type == 'CHAR' or token.type == 'BOOL':
            if GlobalVariables.arrCheckValue(token.value, GlobalVariables.type_flag):
                GlobalVariables.array_values.append(token.value)
                GlobalVariables.state -= 1
            else:
                print("ERROR: Variable no es del mismo tipo ",GlobalVariables.type_flag)
                sys.exit(2)

        else:
            print("ERROR: Esperaba un valor")
            sys.exit(2)

    # Terminar asignacion
    elif GlobalVariables.state == 6:
        if token.type == ';':
            #Ya terminó el programa
            print('Ya terminé!',GlobalVariables.type_flag,GlobalVariables.current_variable_ID,'el tamaño es de:',len(GlobalVariables.array_values))
            GlobalVariables.symbol_table[GlobalVariables.current_variable_ID] = {
                "type": GlobalVariables.type_flag,
                "size": len(GlobalVariables.array_values),
                "value": GlobalVariables.array_values
            }
            resetFlags()

        else:
            print('Error de sintáxis: esperaba un ASSIGN o un ;')
            sys.exit(2)

