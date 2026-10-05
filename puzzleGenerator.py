# each queen takes a turn in choosing a random space to expand into? - not unique :( its okay lets do it anyway

from base import Board, Cell
import random

board = Board(5)

def _find_forbidden_cells(board: Board, queen: dict):
    # add Vertical
    col = queen["col"]
    row = queen["row"]
    forbidden_cells = set()
    forbidden_cells.update(board.cells[row])
    
    for i in range(board.size):
        forbidden_cells.add(board.cells[i][col])
        
    for i in range(4):
        col_addifier = -1 if i % 2 == 0 else 1
        row_addifier = 1 if i < 2 else -1
        r = row + row_addifier
        c = col + col_addifier
        if not r < 0 and not c < 0 and not r >= board.size and not c >= board.size:
            forbidden_cells.add(board.cells[row+row_addifier][col+col_addifier])
    
    return forbidden_cells

def queen_setter(board: Board):
    forbidden_cells: set[Cell] = set()
    queen_list = []
    for queen in range(board.size):
        suitable_cell_chosen = False

        while not suitable_cell_chosen:
            if len(forbidden_cells) == board.size**2:
                raise
            random_row = random.choice(board.cells)
            random_cell = random.choice(random_row)
            if random_cell not in forbidden_cells: # O(1) cah we using a set
                suitable_cell_chosen = True
                
        queen_obj = {"row": random_cell.row, "col": random_cell.col, "region": queen}
        queen_list.append(queen_obj)
        forbidden_set = _find_forbidden_cells(board, queen_obj)
        forbidden_cells.update(forbidden_set)
    return queen_list
        
def surrounding_cells(board: Board, row: int, col: int):
    candidates: set[Cell] = set()
    for adj_cell in range(4):
        row_addifier = (adj_cell % 2)-1 if not adj_cell == 2 else 1 # -1, 0, 1, 0
        col_addifier = ((adj_cell + 1) % 2) - 1 if not adj_cell == 3 else 1 # 0, -1, 0, 1
        r = row + row_addifier
        c = col + col_addifier
        if 0 <= r < board.size and 0 <= c < board.size:
            if board.cells[r][c].region == -1:
                candidates.add(board.cells[r][c])
            
    return candidates

def region_creator(board: Board, queen_list: list):
    # initial candidate creation
    candidates_per_queen: list[set[Cell]] = []
    for queen in range(board.size):
        queen_cell = board.cells[queen_list[queen]["row"]][queen_list[queen]["col"]]
        queen_cell.region = queen
        queen_list[queen]["region"] = queen
        candidates_per_queen.append(
            surrounding_cells(board, queen_list[queen]["row"], 
                              queen_list[queen]["col"]))
    
    q_iterator = 0
    for row in range(board.size):
        for col in range(board.size):
            # chooses a random candidate for whichever queen's turn it is
            the_chosen_one = random.choice(tuple(candidates_per_queen[q_iterator]))
            for candidates in candidates_per_queen:
                candidates.discard(the_chosen_one)
            the_chosen_one.region = q_iterator
            candidates_per_queen[q_iterator].update(
                surrounding_cells(board, the_chosen_one.row, the_chosen_one.col))
            q_iterator = (q_iterator + 1) % board.size
            
            
        