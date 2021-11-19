import sys

# Symbol Table
symbol_table = {}

# Global variables | Flags
start_flag = False
end_flag = False

# Array
array_values = []

# Flags for Variables
assign_variable_flag = False
assign_array_flag = False
type_flag = ''
state = 0
current_variable_ID = ''
current_variable_value = ''
current_operator = ''
modify_existing_varaible_flag = False

# Global Functions

# Funcion para checar si el valor cumple con el tipo de la variable
def arrCheckValue(value, type):
    if type == 'INTEGER' and isinstance(value, int):
        return True
    elif type == 'FLOAT' and isinstance(value, float):
        return True
    else:
        return False

def checkIfVariableIsDefined(token):
    global symbol_table
    if token.value in symbol_table.keys():
        return True
    else:
        print("Error in line",token.lineno,":  Variable ",token.value,' is not defined.')
        sys.exit(2)