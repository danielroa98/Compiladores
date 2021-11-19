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

# Function flags
declare_function_flag = False
function_arg_type = ''
function_args = []

# Print flags
print_in_line_flag = False
print_in_newline_flag = False

# While loop and If variables

# If flags
if_flag = False

# While flags
while_loop_flag = False

# General variables for While and If
var1_type = ''
var1_value = ''
comparacion = ''
var2_type = ''
var2_value = ''

# Global Functions

def checkValue(value, type):
    """ 
        Function checkValue
        Receives:
            value: the second token's value to be checked and verified.
            type: the first token's type to validate they are the same.
        Returns:
            True: in case they are the same data types.
            False: in case they are not the same data types. 
    """
    print(value,type)
    if type == 'INT_TYPE' and isinstance(value, int):
        return True
    elif type == 'FLOAT_TYPE' and isinstance(value, float):
        return True
    else:
        return False

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

def logicalOperations(var1, var2, operator):
    """ 
    Additional information:

    EQ -> r'=='

    LE -> r'<='

    LT -> r'<'

    GE -> r'>='

    GT -> r'>'

    NE -> r'!='
    """
    # print(operator)
    if operator == 'EQ':
        if var1 == var2:
            return True
        else:
            return False
    elif operator == 'LE':
        if var1 <= var2:
            return True
        else:
            return False
    elif operator == 'LT':
        if var1 < var2:
            return True
        else:
            return False
    elif operator == 'GE':
        if var1 >= var2:
            return True
        else:
            return False
    elif operator == 'GT':
        if var1 > var2:
            return True
        else:
            return False
    elif operator == 'NE':
        if var1 != var2:
            return True
        else:
            return False