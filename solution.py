import itertools

rows = 'ABCDEFGHI'
cols = '123456789'


assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

def prod(A,B):
    return [A[index]+B[index] for index,item in enumerate(B)]
        

boxes = cross(rows, cols) #Get all 81 boxes annotated
row_units = [cross(r,cols) for r in rows] #Get rows (horizontal)
col_units = [cross(rows,c) for c in cols] #get columns (Vertical)
diag_units = [prod(rows,cols),prod(rows,cols[::-1])] #Get the diagonal boxes for the Diagonal Sudoku
square_units = [cross(rs,cl) for rs in ('ABC','DEF','GHI') for cl in ('123','456','789')] #Get the 9 square units 
unitlist = row_units + col_units + square_units + diag_units #All the units 
units = dict((s, [u for u in unitlist if s in u]) for s in boxes) #Get a dictionary Box: Units 
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) #set so that duplicates are not added, get a dictionary Box: #Peers in the same unit


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        #find boxes with 2 digits
        pairs = [box for box in unit if len(values[box])==2]
        
        candidate_pairs = [list(pair) for pair in itertools.combinations(pairs, 2)] #for flipped values
        for pair in candidate_pairs:
            box1 = pair[0]
            box2 = pair[1]
            
            #match the values to find the naked twins
            if values[box1] == values[box2]:
                for box in unit:
                    #elimination
                    if box!= box1 and box!= box2:
                        for digit in values[box2]:
                            values[box] = values[box].replace(digit,'')
    return values
    
                        
                    


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #Convert grid into a dict of {square: char} with '123456789' for empties.
    values = grid_values(grid)
    solved = search(values)
    if solved:
        return solved
    else:
        return False

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
