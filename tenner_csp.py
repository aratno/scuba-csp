#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools
import re

def var_from_entry(val, row, col):
    '''
    Takes a value in {-1,..,9} and row-col coordinates and returns a variable for it.
    '''
    if val == -1:
        domain = list(range(10))
    else:
        domain = [val]
    ret = Variable('({},{})'.format(row, col), domain=domain)

    # Pre-filled values are already assigned
    #    if val != -1:
    #        ret.assign(val)

    return ret

def coords(var):
    '''
    Retrieves the coordinates from the name of var (hacky, I know).
    '''
    m = re.match('^.*\((\d+),(\d+)\)$', var.name)
    return int(m.group(1)), int(m.group(2))

def in_range(t1, t2):
    t1 = tuple(t1)
    t2 = tuple(t2)
    if len(t1) != 2 or len(t2) != 2:
        raise Exception('Must be coords in R2')
    else:
        # Return bottom 3 neighbours
        return (t1[0]+1 == t2[0]) and abs(t1[1] - t2[1]) <= 1
        # Return surrounding 8 neighbours
        # return abs(t1[0] - t2[0]) <= 1 and abs(t1[1] - t2[1]) <= 1

def neighbours_of(var, others):
    '''
    Gets neighbours of var in list others, as dictated by in_range predicate
    '''
    print('Finding neighbours of {}'.format(var))

    center = coords(var)
    print('Found coords of {var} to be {center}'.format(var=var, center=center))
    neighbs = []
    for v in others:
        if in_range(center, coords(v)) and center != coords(v):
            print('Variable {} is in range of center'.format(v))
            neighbs.append(v)

    return neighbs

def tenner_csp_model_1(initial_tenner_board):
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
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    # IMPLEMENT
    # Basic inspection
    print('Board')
    for row in initial_tenner_board[0]:
        print(row)
    print('Solution')
    print(initial_tenner_board[1])

    # Create all variables
    print('Creating variable array')
    variable_array = []
    for i, row in enumerate(initial_tenner_board[0]):
        row_vars = []
        for j, entry in enumerate(row):
            var = var_from_entry(entry, i, j)
            print('Adding var {} with assignment {}'.format(var, var.get_assigned_value()))
            row_vars.append(var)
            #print('Created variable {var.name} with domain {var.dom}'.format(var=var))
        variable_array.append(row_vars)
    print('Variable array (flattened): {}'.format(itertools.chain(*variable_array)))

    csp = CSP('Model-1-CSP', vars=list(itertools.chain(*variable_array)))

    # Create all-diff constraints
    # One constraint per unassigned item
    # for var in filter(lambda v: not v.is_assigned(), list(itertools.chain(*variable_array))):
    for var in itertools.chain(*variable_array):
        # Scope is all pairs from neighboring variables
        neighbours = neighbours_of(var, itertools.chain(*variable_array))
        for neighbour in neighbours:
            c = Constraint(name=None, scope=[var, neighbour])
            # Create satisfying tuples
            # Only use values in domain of variable, neighbour
            # c.add_satisfying_tuples(itertools.permutations(range(10), 2))
            sat_tups = list(pair for pair in itertools.product(var.cur_domain(), neighbour.cur_domain()) if len(set(pair)) == len(pair))
            print('Adding all-diff tuples {tups} for variables {vars}'.format(tups=sat_tups, vars=[var,neighbour]))
            c.add_satisfying_tuples(sat_tups)
            csp.add_constraint(c)

    # Create row constraints
    for row in variable_array:
        for pair in itertools.combinations(row, 2):
            print('Row pair is {}'.format(pair))
            c = Constraint(name=None, scope=pair)
            sat_tups = list(vals for vals in itertools.product(pair[0].cur_domain(), pair[1].cur_domain()) if len(set(vals)) == len(vals))
            c.add_satisfying_tuples(sat_tups)
            csp.add_constraint(c)

    # Create sum constraints over columns
    for col_num, col in enumerate(zip(*variable_array)):
        domains = [list(var.cur_domain()) for var in col]
        # All sums
        sat_sums = [tup for tup in itertools.product(*domains) if sum(tup) == initial_tenner_board[1][col_num]]
        print('Column {} needs to sum to {}'.format(col_num, initial_tenner_board[1][col_num]))
        print('{} possible sums'.format(len(list(sat_sums))))
        c = Constraint(name=None, scope=list(col))
        c.add_satisfying_tuples(sat_sums)
        csp.add_constraint(c)

    print('csp = {}\nvariable_array = {}'.format(csp, variable_array))
    return csp, variable_array

def tenner_csp_model_2(initial_tenner_board):
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

    '''
    README:
    Because my part I is not working for unknown reasons (I've been staring at
    it for the last two days straight, with no results), I'll just post some
    notes here on how I _would_ do part II, and hope that suffices for some
    portion of credit.

    The difference between part I and part II is the all-diff n-ary constraint
    on rows. In part I, the binary all-diff constraints are generated with a
    set of tuples for every pair of variables, such that the values were
    different. This was achieved with:
        itertools.permutations(range(10), 2)

    To replace this with an n-ary constraint, there should be a single constraint
    over each row (as opposed to each pair of unique elements in a row), and that
    can be done with the following generator:
        (tup for tup in itertools.product(*domains) if len(set(tup)) == len(tup))
    This conditional ensures uniqueness of elements. If there are any duplicate
    elements in tup, the set will not consider them, leaving a smaller length.

    This is the only change necessary. The following code reflects this change.

    JK. Now it works!
    '''
    # Basic inspection
    print('Board')
    for row in initial_tenner_board[0]:
        print(row)
    print('Solution')
    print(initial_tenner_board[1])

    # Create all variables
    print('Creating variable array')
    variable_array = []
    for i, row in enumerate(initial_tenner_board[0]):
        row_vars = []
        for j, entry in enumerate(row):
            var = var_from_entry(entry, i, j)
            #print('Adding var {} with assignment {}'.format(var, var.get_assigned_value()))
            row_vars.append(var)
            #print('Created variable {var.name} with domain {var.dom}'.format(var=var))
        variable_array.append(row_vars)
    print('Variables (flattened): {}'.format(list(itertools.chain(*variable_array))))

    csp = CSP('Model-1-CSP', vars=list(itertools.chain(*variable_array)))

    # Create all-diff constraints
    # One constraint per unassigned item
    # for var in filter(lambda v: not v.is_assigned(), list(itertools.chain(*variable_array))):
    for var in itertools.chain(*variable_array):
        # Scope is all pairs from neighboring variables
        neighbours = neighbours_of(var, list(itertools.chain(*variable_array)))
        for neighbour in neighbours:
            c = Constraint(name=None, scope=[var, neighbour])
            # Create satisfying tuples
            # Only use values in domain of variable, neighbour
            # c.add_satisfying_tuples(itertools.permutations(range(10), 2))
            sat_tups = list(pair for pair in itertools.product(var.cur_domain(), neighbour.cur_domain()) if pair[0] != pair[1])
            #print('Adding all-diff tuples {tups} for variables {vars}'.format(tups=sat_tups, vars=[var,neighbour]))
            c.add_satisfying_tuples(sat_tups)
            csp.add_constraint(c)

    # Create row constraints
    for row in variable_array:
        domains = [list(var.cur_domain()) for var in row]
        c = Constraint(name=None, scope=row)
        c.add_satisfying_tuples(list(tup for tup in itertools.product(*domains) if len(set(tup)) == len(tup)))
        csp.add_constraint(c)

    # Create sum constraints over columns
    for col_num, col in enumerate(zip(*variable_array)):
        domains = [list(var.cur_domain()) for var in col]
        # All sums
        sat_sums = [tup for tup in itertools.product(*domains) if sum(tup) == initial_tenner_board[1][col_num]]
        #print('Column {} needs to sum to {}'.format(col_num, initial_tenner_board[1][col_num]))
        #print('{} possible sums'.format(len(list(sat_sums))))
        c = Constraint(name=None, scope=list(col))
        c.add_satisfying_tuples(sat_sums)
        csp.add_constraint(c)

    print('Returning CSP ')
    csp.print_all()
    print('Returning variable_array {}'.format(variable_array))
    for var in csp.get_all_vars():
        print(var, var.is_assigned(), '\n')
    return csp, variable_array
