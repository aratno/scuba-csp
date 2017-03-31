#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:49:40 2017

@author: aaronboswell
"""
    
import signal

from cspbase import *
from puzzles import *
from propagators import *

def try_to_solve(initial_sudoku_puzzle):
    for row in rows(initial_sudoku_puzzle):
        if len(set(cell for cell in row if cell != 0)) != len([cell for cell in row if cell != 0]):
            return False
    for column in columns(initial_sudoku_puzzle):
        if len(set(cell for cell in column if cell != 0)) != len([cell for cell in column if cell != 0]):
            return False
    for cage in cages(initial_sudoku_puzzle):
        if len(set(cell for cell in cage if cell != 0)) != len([cell for cell in cage if cell != 0]):
            return False
        
    csp = sudoku_model_1(initial_sudoku_puzzle)
    
    solver = BT(csp)
    solver.bt_search(prop_GAC)
    
def sudoku_model_1(initial_sudoku_puzzle):
    
    variable_array = [Variable(str(i), [initial_sudoku_puzzle[i]]) for i in range(len(initial_sudoku_puzzle))]

    for i in range(len(variable_array)):
        if initial_sudoku_puzzle[i] == 0:
                variable_array[i]= Variable(str(i) , [n for n in range(1,10)])

    csp = CSP("Sudoku_model_1", variable_array)
    #row constraints
    row_array = rows(variable_array)
    add_array_constraint(row_array, csp, "row")
    #column constraints  
    column_array = columns(variable_array)
    add_array_constraint(column_array, csp, "column")
    #cage constraints
    cage_array = cages(variable_array)
    add_array_constraint(cage_array, csp, "cage")
    
    return csp
    
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

if __name__ == '__main__':
    puzzle = test_problem_1
    try_to_solve(puzzle)
