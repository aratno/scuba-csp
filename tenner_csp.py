#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def tenner_csp_model_1(initial_tenner_board):
    start_array = initial_tenner_board[0]
    variable_array = [[Variable(str(i) + ',' + str(j), [n for n in range(10)]) for i in range(10)] for j in range(len(start_array))]
    for i in range(0,len(start_array)):
        for j in range(0,10):
            if start_array[i][j] != -1:
                variable_array[i][j]= Variable(str(i) + ',' + str(j), [start_array[i][j]])
    flat = [x for sublist in variable_array for x in sublist]

    csp = CSP("model_1", flat)
    #row constraints

    for row_num in range(len(variable_array)):
        row = variable_array[row_num]
        for i in range(len(row)):
            for j in range(i+1, len(row)):
                pred = (lambda a, b: all(a in row[i].domain(), b in row[j].domain(), a != b))
                con = Constraint(str(row_num) + ',' + str(i) +';' + str(row_num) + ',' + str(j), [row[i],row[j]], pred)
                csp.add_constraint(con)
    #adjacent constraints
    added_strings = []
    for row_num in range(len(variable_array)):
        row = variable_array[row_num]
        for column_num in range(len(row)):
            spot = (row_num,column_num)
            for neighbor in neighbor_tuples(len(variable_array),len(row),spot):
                v1 = (row_num, column_num)
                v2 = neighbor
                if v1[0] < v2[0]:
                    v2 = v1
                    v1 = neighbor
                elif v1[0] == v2[0]:
                    if v1[1] < v2[1]:
                        v2 = v1
                        v1 = neighbor
                string = str(v1[0]) + ',' + str(v1[1]) +';' + str(v2[0]) + ',' + str(v2[1])   
                if string in added_strings:
                    continue
                added_strings.append(string)
                variable1 = variable_array[v1[0]][v1[1]]
                variable2 = variable_array[v2[0]][v2[1]]
                #TODO make it so it does not add unnessicary constraints

                pred = (lambda a, b: all(a in variable1.domain(), b in variable2.domain(), a != b))
                con = Constraint(string, [variable1, variable2], pred)
                csp.add_constraint(con)

    #sum constraints
    for column_num in range(10):

        current_column = []
        for row_num in range(len(variable_array)):
            current_column.append(variable_array[row_num][column_num])
        # TODO: This is a complex line, let me know if you want clarifications.
        pred = (lambda *args: (all(val in var.domain() for val, var in zip(args, current_column))) and (sum(args) == initial_tenner_board[1][column_num]))
        con = Constraint("column:" + str(column_num), current_column, pred)

        column_desired_sum = initial_tenner_board[1][column_num]
        tuples = []
        domains = []
        for variable in current_column:
            domains.append(variable.domain())
        for t in itertools.product(*domains):
            if sum(t) == column_desired_sum:
                   tuples.append(t)
        con.add_satisfying_tuples(tuples)
        csp.add_constraint(con) 

    
    return csp, variable_array

def neighbor_tuples(max_x, max_y, spot):
    neighbors = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            new = (spot[0] + x, spot[1] + y)
            if new != spot:
                if -1 < new[0] < max_x:
                    if -1 < new[1] < max_y:
                        neighbors.append(new)
    return neighbors

    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a -1 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    
#IMPLEMENT

##############################
def all_unique(t):
    seen = []
    for element in t:
        if element in seen:
            return False
        seen.append(element)
    return True
def tenner_csp_model_2(initial_tenner_board):
    
    start_array = initial_tenner_board[0]
    variable_array = [[Variable(str(i) + ',' + str(j), [n for n in range(10)]) for i in range(10)] for j in range(len(start_array))]
    for i in range(0,len(start_array)):
        for j in range(0,10):
            if start_array[i][j] != -1:
                variable_array[i][j]= Variable(str(i) + ',' + str(j), [start_array[i][j]])
    flat = [x for sublist in variable_array for x in sublist]

    csp = CSP("model_2", flat)
    #row constraints

    for row_num in range(len(variable_array)):
        row = variable_array[row_num]

        pred = (lambda *args: all(val in var.domain() for val, var in zip(args, row)) and len(set(args)) == len(args))
        con = Constraint("row:" +  str(row_num), row, pred)
        domains = []
        for variable in row:
            domains.append(variable.domain())
            
        tuples = []
        for t in itertools.product(*domains):
            if all_unique(t):
                tuples.append(t)
        con.add_satisfying_tuples(tuples)
        csp.add_constraint(con)
    #adjacent constraints
    added_strings = []
    for row_num in range(len(variable_array)):
        row = variable_array[row_num]
        for column_num in range(len(row)):
            spot = (row_num,column_num)
            for neighbor in neighbor_tuples(len(variable_array),len(row),spot):
                v1 = (row_num, column_num)
                v2 = neighbor
                if v1[0] < v2[0]:
                    v2 = v1
                    v1 = neighbor
                elif v1[0] == v2[0]:
                    if v1[1] < v2[1]:
                        v2 = v1
                        v1 = neighbor
                string = str(v1[0]) + ',' + str(v1[1]) +';' + str(v2[0]) + ',' + str(v2[1])   
                if string in added_strings:
                    continue
                added_strings.append(string)
                variable1 = variable_array[v1[0]][v1[1]]
                variable2 = variable_array[v2[0]][v2[1]]
                #TODO make it so it does not add unnessicary constraints

                pred = (lambda a, b: all(a in variable1.domain(), b in variable2.domain()) and a != b)
                con = Constraint(string, [variable1, variable2], pred)
                tuples = []
                for t in itertools.product(variable1.domain(), variable2.domain()):
                    if t[0] != t[1]:
                        tuples.append(t)
                con.add_satisfying_tuples(tuples)
                csp.add_constraint(con)
    #sum constraints
    for column_num in range(10):

        current_column = []
        for row_num in range(len(variable_array)):
            current_column.append(variable_array[row_num][column_num])
        con = Constraint("column:" + str(column_num),current_column )

        column_desired_sum = initial_tenner_board[1][column_num]
        tuples = []
        domains = []
        for variable in current_column:
            domains.append(variable.domain())
        for t in itertools.product(*domains):
            if sum(t) == column_desired_sum:
                   tuples.append(t)
        con.add_satisfying_tuples(tuples)
        csp.add_constraint(con) 

    
    return csp, variable_array
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular,
       model_2 has a combination of n-nary 
       all-different constraints and binary not-equal constraints: all-different 
       constraints for the variables in each row, binary constraints for  
       contiguous cells (including diagonally contiguous cells), and n-nary sum 
       constraints for each column. 
       Each n-ary all-different constraint has more than two variables (some of 
       these variables will have a single value in their domain). 
       model_2 should create these all-different constraints between the relevant 
       variables.
    '''

#IMPLEMENT
