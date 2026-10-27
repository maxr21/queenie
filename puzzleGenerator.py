from base import Board, Cell, Queen
import random

def surrounding_diag(board: Board, row: int, col: int) -> set[Cell]:
    '''gets the four diagonals of a given row, int on a board'''
    candidates = set()
    for i in range(4):
        col_addifier = -1 if i % 2 == 0 else 1
        row_addifier = 1 if i < 2 else -1
        r = row + row_addifier
        c = col + col_addifier
        if not r < 0 and not c < 0 and not r >= board.size and not c >= board.size:
            candidates.add(board.cells[row+row_addifier][col+col_addifier])
    return candidates

def _find_forbidden_cells(board: Board, queen: Queen) -> set[Cell]:
    '''Given a board and a single queen, returns a set of cells that are attacked 
    by that individual queen on the board'''
    # add Vertical
    col = queen.col
    row = queen.row
    forbidden_cells = set()
    forbidden_cells.update(board.cells[row])
    
    for i in range(board.size):
        forbidden_cells.add(board.cells[i][col])
    
    forbidden_cells.union(surrounding_diag(board, row, col))
    
    return forbidden_cells

def queen_setter(board: Board) -> list[Queen]:
    '''Given a board, returns a list of queen objects placed 
    such that they do not attack each other.'''
    forbidden_cells: set[Cell] = set()
    queen_list = []
    for queen in range(board.size):
        suitable_cell_chosen = False

        while not suitable_cell_chosen: # COULD BE WAY MORE EFFICIENT - if difference between forbidden cells set and board set.
            random_row = random.choice(board.cells)
            random_cell = random.choice(random_row)
            # print(f"chosen cell: {random_cell}")
            if random_cell not in forbidden_cells: # O(1) cah we using a set
                # print(f"placing queen {queen} in cell ({random_cell})")
                suitable_cell_chosen = True
            if len(forbidden_cells) == board.size**2:
                return queen_setter(board)
        
        queen_obj = Queen(row=random_cell.row, col=random_cell.col, region=queen)
        queen_list.append(queen_obj)
        forbidden_set = _find_forbidden_cells(board, queen_obj)
        forbidden_cells.update(forbidden_set)
    return queen_list

def surrounding_cells(board: Board, row: int, col: int) -> set[Cell]:
    '''returns a set of cells of the four non-diagonal surrounding cells of the input row, col'''
    candidates: set[Cell] = set()
    for adj_cell in range(4):
        row_addifier = (adj_cell % 2)-1 if not adj_cell == 2 else 1 # -1, 0, 1, 0
        col_addifier = ((adj_cell + 1) % 2) - 1 if not adj_cell == 3 else 1 # 0, -1, 0, 1
        r = row + row_addifier
        c = col + col_addifier
        if 0 <= r < board.size and 0 <= c < board.size:
            # print(f"({r}, {c}) - board cell: {board.cells[r][c]}")
            candidates.add(board.cells[r][c])
            
    return candidates

def filter_out_regioned(candidates: set) -> set[Cell]:
    '''given a set of cells, it removes any cell within the set that has a region'''
    real_candidates = set()
    for candidate in candidates:
        if candidate.region == -1:
            real_candidates.add(candidate)
    return real_candidates
    
def region_creator(board: Board, queen_list: list[Queen]) -> None:
    '''Given a board and a COMPLETE list of queens, 
    assigns each queen and cell on the board a region
    INVARIANTS - queen list is complete
     - Cells on the board have no regions assigned
     - queen_list is a valid queen_list for the input board'''
    # initial candidate creation
    candidates_per_queen: list[set[Cell]] = []
    for queen in range(board.size):
        queen_cell = board.cells[queen_list[queen].row][queen_list[queen].col]
        queen_cell.region = queen
        queen_list[queen].region = queen
        candidates = filter_out_regioned(surrounding_cells(board, queen_list[queen].row, 
                              queen_list[queen].col))
        candidates_per_queen.append(candidates)
    q_iterator = 0
    cells_to_assign = board.size**2 - board.size
    i = 0
    while i < cells_to_assign: # assign every cell a region
        # chooses a random candidate for whichever queen's turn it is
        # print(q_iterator)
        if not len(candidates_per_queen[q_iterator]) == 0:
            i += 1
            the_chosen_one = random.choice(tuple(candidates_per_queen[q_iterator]))
            the_chosen_one.region = q_iterator
            # print(f'added cell {the_chosen_one} to queen {q_iterator}')
            candidates_per_queen[q_iterator].update(
                filter_out_regioned(surrounding_cells(board, the_chosen_one.row, the_chosen_one.col)))
            
            for candidates in candidates_per_queen:
                candidates.discard(the_chosen_one)
            
        q_iterator = (q_iterator + 1) % board.size
