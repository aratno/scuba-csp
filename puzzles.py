import itertools

test_problem_1 = [
        5,3,0,0,7,0,0,0,0, \
        6,0,0,1,9,5,0,0,0, \
        0,9,8,0,0,0,0,6,0, \
        8,0,0,0,6,0,0,0,3, \
        4,0,0,8,0,3,0,0,1, \
        7,0,0,0,2,0,0,0,6, \
        0,6,0,0,0,0,2,8,0, \
        0,0,0,4,1,9,0,0,5, \
        0,0,0,0,8,0,0,7,9]
'''
530 070 000
600 195 000
098 000 060

800 060 003
400 803 001
700 020 006

060 000 280
000 419 005
000 080 079
'''

test_solution_1 = [
        5,3,4,6,7,8,9,1,2, \
        6,7,2,1,9,5,3,4,8, \
        1,9,8,3,4,2,5,6,7, \
        8,5,9,7,6,1,4,2,3, \
        4,2,6,8,5,3,7,9,1, \
        7,1,3,9,2,4,8,5,6, \
        9,6,1,5,3,7,2,8,4, \
        2,8,7,4,1,9,6,3,5, \
        3,4,5,2,8,6,1,7,9]
'''
534 678 912
672 195 348
198 342 567

859 761 423
426 853 791
713 924 856

961 537 284
287 419 635
345 286 179
'''

def is_well_formed(puzzle):
    '''
    Takes a sudoku puzzle in the form of a 1D array, and verifies that
    it is well-formed. Well-formed puzzles have 81 entries, each in
    range(10).
    '''
    return all(cell in range(0, 10) for cell in puzzle) and len(puzzle) == 81

def _grouper(iterable, n, fillvalue=None):
    '''
    Collect data into fixed-length chunks or blocks.
    From itertools recipes.
    '''
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def rows(puzzle):
    if not is_well_formed(puzzle):
        raise Exception('Puzzle is not well-formed')
    else:
        return _grouper(puzzle, 9, fillvalue=None)

def columns(puzzle):
    if not is_well_formed(puzzle):
        raise Exception('Puzzle is not well-formed')
    else:
        return map(lambda *args: tuple(arg for arg in args), *_grouper(puzzle, 9, fillvalue=None))

def cages(puzzle):
    if not is_well_formed(puzzle):
        raise Exception('Puzzle is not well-formed')
    else:
        for cage_num in range(0, 9):
            offset = 3 * (cage_num % 3) + 27 * (cage_num // 3)
            yield tuple([puzzle[0+offset], puzzle[1+offset], puzzle[2+offset],
                    puzzle[9+offset], puzzle[10+offset], puzzle[11+offset],
                    puzzle[18+offset], puzzle[19+offset], puzzle[20+offset]])

if __name__ == '__main__':
    import pprint
    pprint.pprint(list(rows(test_problem_1)))
    pprint.pprint(list(cages(test_problem_1)))
