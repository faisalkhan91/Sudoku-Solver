#!/usr/bin/python3

#############################################################################################
#                               Program by Mohammed Faisal Khan                             #
#                               00598949                                                    #
#                               mkhan8@unh.newhaven.edu                                     #
#                               Created on March 4, 2018                                 #
#############################################################################################

# References
# http://norvig.com/sudoku.html

# Importing modules

# Function Definitions


def test():
    """A set of unit tests."""
    assert len(squares) == 36
    assert len(unitlist) == 18
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 12 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6'],
                           ['C1', 'C2', 'C3', 'D1', 'D2', 'D3']]
    assert peers['C2'] == set(['A2', 'C3', 'B2', 'C4', 'D3', 'C5', 'D1', 'C1', 'C6', 'F2', 'E2', 'D2'])
    print('All tests pass.', end="\n")


def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [a+b for a in A for b in B]


def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    # To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False  # (Fail if we can't assign d to square s.)
    return values


def grid_values(grid):
    """Convert grid into a dict of {square: char} with '0' or '.' for empties."""
    chars = [c for c in grid if c in digits or c in '0.']
    # print(chars)
    assert len(chars) == 36
    return dict(zip(squares, chars))


def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values  # Already eliminated
    values[s] = values[s].replace(d, '')
    # (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False  # Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    # (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  # Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


def display(values):
    # print(values, end="\n")
    """Display these values as a 2-D grid."""
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*2)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '3' else '')
                      for c in cols))
        if r in 'BD':
            print(line)
    print()

#############################################################################################

# Main Program


digits = '123456'
letters = 'ABCDEF'
rows = letters
cols = digits

squares = cross(rows, cols)
# print(squares, end="\n")

unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('AB', 'CD', 'EF') for cs in ('123', '456')])
# print(unitlist, end="\n")

units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
# print(units['C2'], end="\n")

peers = dict((s, set(sum(units[s], []))-set([s]))
             for s in squares)
# print(peers['C2'], end="\n")

# test()

# grid1 = '210045003001025400134000000130040562'
# print(len(grid1), end="\n")

grid = str(input("Enter the Sudoku grid you want to solve (indicate blank spaces with 0 or .): "))

display(parse_grid(grid))

#############################################################################################
#                                       End of Program                                      #
#                                     Copyright (c) 2018                                    #
#############################################################################################
