#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:49:40 2017

@author: aaronboswell
"""
    
import signal
import itertools
import random
import pprint
import functools
from datetime import datetime

from cspbase import *
from puzzles import *
from propagators import *

def try_to_solve(initial_sudoku_puzzle):
    csp = sudoku_model_1(initial_sudoku_puzzle)
    
    solver = BT(csp)
    return solver.bt_search(prop_GAC) , csp
 
def sudoku_model_1(initial_sudoku_puzzle):
    print('Creating variables...')
    variable_array = [Variable(str(i), [initial_sudoku_puzzle[i]]) for i in range(len(initial_sudoku_puzzle))]

    for i in range(len(variable_array)):
        if initial_sudoku_puzzle[i] == 0:
                variable_array[i]= Variable(str(i) , [n for n in range(1,10)])
    print('Done creating variables.')

    csp = CSP("Sudoku_model_1", variable_array)
    
    #row constraints
    print('Adding row constraints...')
    row_array = rows(variable_array)
    add_array_constraint(row_array, csp, "row")
    
    #column constraints  
    print('Adding column constraints...')
    column_array = columns(variable_array)
    add_array_constraint(column_array, csp, "column")
    
    #cage constraints
    print('Adding cage constraints...')
    cage_array = cages(variable_array)
    add_array_constraint(cage_array, csp, "cage")
    
    print('Generated CSP with {} satisfying tuples'.format(functools.reduce(lambda ac, v: ac + len(v), list(map(lambda c: c.sat_tuples, csp.get_all_cons())), 0)))
    return csp
    
def verify(initial_sudoku_puzzle):
    
    for row in rows(initial_sudoku_puzzle):
        if len(set(cell for cell in row if cell != 0)) != len([cell for cell in row if cell != 0]):
            return False
    for column in columns(initial_sudoku_puzzle):
        if len(set(cell for cell in column if cell != 0)) != len([cell for cell in column if cell != 0]):
            return False
    for cage in cages(initial_sudoku_puzzle):
        if len(set(cell for cell in cage if cell != 0)) != len([cell for cell in cage if cell != 0]):
            return False
    return True
    

def homogeneity(initial_sudoku_puzzle):
    minimum = 10
    maximum = 0
    for row in rows(initial_sudoku_puzzle):
        minimum = min( minimum, len(set(cell for cell in row if cell != 0))) 
        maximum = max( maximum, len(set(cell for cell in row if cell != 0))) 

    for column in columns(initial_sudoku_puzzle):
        minimum = min( minimum, len(set(cell for cell in column if cell != 0))) 
        maximum = max( maximum, len(set(cell for cell in column if cell != 0))) 
        
    for cage in cages(initial_sudoku_puzzle):
        minimum = min( minimum, len(set(cell for cell in cage if cell != 0))) 
        maximum = max( maximum, len(set(cell for cell in cage if cell != 0))) 
    return maximum - minimum + 1

def two_in_everything(initial_sudoku_puzzle):
    for row in rows(initial_sudoku_puzzle):
        if len([cell for cell in row if cell != 0]) < 2:
            return False
    for column in columns(initial_sudoku_puzzle):
        if len([cell for cell in column if cell != 0]) < 2:
            return False
    for cage in cages(initial_sudoku_puzzle):
        if len([cell for cell in cage if cell != 0]) < 2:
            return False
    return True

def create_random_diagonal_puzzle():
    return puzzle_from_cages([random.choice(list(itertools.permutations(range(1, 10)))),
                               list(itertools.repeat(0, 9)),
                               list(itertools.repeat(0, 9)),
                               list(itertools.repeat(0, 9)),
                               random.choice(list(itertools.permutations(range(1, 10)))),
                               list(itertools.repeat(0, 9)),
                               list(itertools.repeat(0, 9)),
                               list(itertools.repeat(0, 9)),
                               random.choice(list(itertools.permutations(range(1, 10))))])
    
def create_random_permuted_puzzle(puzzle):
    new_rows = permute_by_3_group(rows(puzzle))
    new_puzzle = list(itertools.chain.from_iterable(new_rows))
    new_columns = permute_by_3_group(columns(puzzle))
    new_puzzle = list(itertools.chain.from_iterable(new_columns))
    new_columns = columns(new_puzzle)
    return list(itertools.chain.from_iterable(new_columns))

def permute_by_3_group(full_groups):
    full_groups = list(full_groups)
    first_group = [full_groups[0],full_groups[1],full_groups[2]]
    second_group = [full_groups[3],full_groups[4],full_groups[5]]
    third_group = [full_groups[6],full_groups[7],full_groups[8]]
    
    random.shuffle(first_group)
    random.shuffle(second_group)
    random.shuffle(third_group)
    return list(itertools.chain.from_iterable([first_group,second_group,third_group]))


def zero_diagonal(puzzle):
    puzzle_rows = list(rows(puzzle))
    for i in range(9):
        puzzle_rows[i][i] = 0
    return list(itertools.chain.from_iterable(puzzle_rows))

def shift_diagonal_puzzle(puzzle):
    puzzle_rows = list(rows(puzzle))
    puzzle_rows[0], puzzle_rows[3], puzzle_rows[6] = puzzle_rows[3], puzzle_rows[6], puzzle_rows[0]
    puzzle_rows[2], puzzle_rows[5], puzzle_rows[8] = puzzle_rows[8], puzzle_rows[2], puzzle_rows[5]
    return list(itertools.chain.from_iterable(puzzle_rows))
    

def create_random_puzzle():
    #puzzle = create_random_diagonal_puzzle()
    puzzle = list(itertools.repeat(0, 81))
    while not two_in_everything(puzzle):
        candidates = list(map(lambda m: m[0], filter(lambda f: f[1] == 0, enumerate(puzzle))))
        elected = random.choice(candidates)
        #print('Elected position {}'.format(elected))
        puzzle[elected] = random.randint(1, 9)
        if not verify(puzzle):
            #print('Position {} with value {} is invalid'.format(elected, puzzle[elected]))
            puzzle[elected] = 0
    num_generated = len(list(filter(lambda f: f != 0, puzzle)))
    #print('Generated puzzle with {} additional values'.format(num_generated))
    return puzzle

def all_unique(t):
    seen = []
    for element in t:
        if element in seen:
            return False
        seen.append(element)
    return True

def add_array_constraint(array, csp, name):
    for position, subarray in enumerate(array):

        con = Constraint(name +  str(position), subarray)
        domains = []
        for variable in subarray:
            domains.append(variable.domain())
            
        tuples = []
        for t in itertools.product(*domains):
            if all_unique(t):
                tuples.append(t)
        con.add_satisfying_tuples(tuples)
        csp.add_constraint(con)
    
# Stolen from StackOverflow
class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)

def t():
    pzs = []
    while len(pzs) < 5:
        print('Starting puzzle at {}'.format(datetime.now()))
        puzzle = create_random_diagonal_puzzle()
        puzzle = shift_diagonal_puzzle(puzzle)
        #puzzle = zero_diagonal(puzzle)
        #puzzle = create_random_puzzle()
        
        status, csp = try_to_solve(puzzle)
        
        if status:
            puzzle = list(itertools.repeat(0, 81))
            
            for i,v in enumerate(csp.vars):
                puzzle[i] =  v.get_assigned_value()
            pzs.append(puzzle)
            print('Puzzle synthesis succeeded')
        else:
            print('Puzzle synthesis failed')
        print('Finishing puzzle at {}'.format(datetime.now()))


    for p in pzs:
        print(p)
if __name__ == '__main__':
    with timeout(seconds = 60*30):
        t()
    
