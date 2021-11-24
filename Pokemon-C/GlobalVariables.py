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
function_tokens = []

run_function_flag = False
function_state = 0

# Struct
declare_struct_flag = False
struct_variable_ID = ''
struct_variables = []

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
var2_type = ''
var2_value = ''
comparacion = ''

# State detector in order to run the operations located inside the IF, ELSE or the WHILE.
inner_operations_state = 0

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
    elif type == 'BOOL_TYPE' and isinstance(value, bool):
        return True
    elif type == 'CHAR_TYPE' and isinstance(value, str):
        return True
    else:
        return False

# Funcion para checar si el valor cumple con el tipo de la variable
def arrCheckValue(value, type):
    if type == 'INTEGER' and isinstance(value, int):
        return True
    elif type == 'FLOAT' and isinstance(value, float):
        return True
    elif type == 'BOOL' and isinstance(value, bool):
        return True
    elif type == 'CHAR' and isinstance(value, str):
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
    Function logicalOperations

    Receives:
        var1: the first variable obtained from the logical operation.
        var2: the second variable obtained from the logical operation.
        operator: the combination of symbols regarding the logical operator that's going to be analysed.
    Returns:
        boolean: This value can either be True or False, depends on the outcome of the operation.


    Additional information:

    EQ -> ==

    LE -> <=

    LT -> <

    GE -> >=

    GT -> >

    NE -> !=
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

