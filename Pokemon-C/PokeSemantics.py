import sys

# Symbol Table Class
class Variable:
    def __init__(self, id, type, value):
        self.id = id
        self.type = type
        self.value = value

# Variables: 
import GlobalVariables

# Analysis functions:
import assign_array
import prints
import runFunction
import loopAndConditionalAnalysis
import functions
import structure
import variables_doc

def init(token):
    programInit(token)

def resetFlags():
    GlobalVariables.assign_variable_flag = False
    GlobalVariables.modify_existing_varaible_flag = False
    GlobalVariables.type_flag = ''
    GlobalVariables.state = 0
    GlobalVariables.current_variable_ID = ''
    GlobalVariables.current_variable_value = ''

def printErr(token, errcode):
    print("Error en el token:", token)
    if errcode == 1:
        print('Error: La batalla aun no inicia.')
    elif errcode == 2:
        print('Error: La batalla ya esta iniciada.')
    elif errcode == 3:
        print('Error: La batalla ya finalizó.')
    elif errcode == 4:
        print('Error: La batalla aun no acaba.')


def programInit(token):
    if token.type == 'START':
        # print(GlobalVariables.start_flag)
        if GlobalVariables.start_flag == True:
            printErr(token, 2)
        else:
            GlobalVariables.start_flag = True
            return
            # print("Changing the start flag:", GlobalVariables.start_flag)
    elif GlobalVariables.start_flag == True:
        
        if GlobalVariables.run_function_flag == True or GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True or GlobalVariables.if_flag == True or GlobalVariables.declare_function_flag == True or GlobalVariables.declare_struct_flag == True or GlobalVariables.while_loop_flag == True:
            #print('No variable detected.')
            print('')
        else:
            variables_doc.variables(token)

        if GlobalVariables.run_function_flag == True or GlobalVariables.assign_variable_flag == True or GlobalVariables.assign_array_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.if_flag == True or GlobalVariables.declare_function_flag == True or GlobalVariables.declare_struct_flag == True or GlobalVariables.while_loop_flag == True:
            #print('No print statement detected.')
            print('')
        else:
            prints.what_print(token)

        if GlobalVariables.run_function_flag == True or GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True or GlobalVariables.assign_variable_flag == True or GlobalVariables.assign_array_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.declare_function_flag == True or GlobalVariables.declare_struct_flag == True:
            #print('No if or while detected.')
            print('')
        else:
            checkLoop(token)
            print('')

        if GlobalVariables.run_function_flag == True or GlobalVariables.assign_variable_flag == True or GlobalVariables.assign_array_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.if_flag == True or GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True or GlobalVariables.declare_struct_flag == True or GlobalVariables.while_loop_flag == True:
        #if 'FINISH' in token:
            #print('No function detected.')
            print('')
        else:
            functions.define_function(token)

        if GlobalVariables.run_function_flag == True or GlobalVariables.assign_variable_flag == True or GlobalVariables.assign_array_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.if_flag == True or GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True or GlobalVariables.while_loop_flag == True:
            #if 'FINISH' in token:
            #print('No structure detected.')
            print('')
        else:
            structure.define_struct(token)

        if GlobalVariables.print_in_line_flag == True or GlobalVariables.print_in_newline_flag == True or GlobalVariables.assign_variable_flag == True or GlobalVariables.assign_array_flag == True or GlobalVariables.modify_existing_varaible_flag == True or GlobalVariables.declare_function_flag == True or GlobalVariables.declare_struct_flag == True:
            #if 'FINISH' in token:
            #print('No function_run detected.')
            print('')
        else:
            #structure.define_struct(token)
            runFunction.run_function(token)
            #print('yay')


        if token.type == 'FINISH':
            programEnd(token)
    else:
        printErr(token, 1)

def checkLoop(token):
    # print("\nWhile flag Status: ", GlobalVariables.while_loop_flag,"If flag status: ", GlobalVariables.if_flag, '\n')
    if GlobalVariables.if_flag == True or GlobalVariables.while_loop_flag == True:
        if GlobalVariables.if_flag == True:
            loopAndConditionalAnalysis.checkIfandElse(token)
            # print('Sending to loopAndConditionalAnalysis file (IF/ELSE)')
        elif GlobalVariables.while_loop_flag == True:
            # print('Sending to loopAndConditionalAnalysis file (WHILE)')
            # print('Sending token', token, 'to WHILE')
            loopAndConditionalAnalysis.whileAnalysis(token)
    else:
        if token.type == 'IF':
            print('Checking IF statement')
            GlobalVariables.if_flag = True
            # print(GlobalVariables.if_flag, 'current value')
        elif token.type == 'WHILE':
            print('Checking WHILE loop')
            GlobalVariables.while_loop_flag = True
            # print(GlobalVariables.while_loop_flag, 'current value')

def programEnd(token):
    
    print('Ending execution')
    #if 'FINISH' in token:
    if token.type == 'FINISH':
        if GlobalVariables.end_flag == True:
            printErr(token, 3)
        else:
            GlobalVariables.end_flag = True
            sys.exit(2)
    else:
        printErr(token, 4)
    # return token

