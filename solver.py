from base import Board, Cell, Queen
from puzzleGenerator import queen_setter, surrounding_diag
import random

from renderer import BoardRenderer
BOARD_SIZE = 8
        
def calculate_loss(board: Board, queen_list: list[Queen]):
    '''calculate the current loss'''
    occupied_regions = set()
    loss = 0
    for queen in queen_list:
        occupied_regions.add(queen.region)
        diag_cells: set[Cell] = surrounding_diag(board, queen.row, queen.col)
        
        for cell in diag_cells:
            for idx in range(len(queen_list)):
                if queen_list[idx].row == cell.row and queen_list[idx].col == cell.col:
                    loss += 1

        #print(f"surrounding for queen ({queen["row"]}, {queen["col"]}): {" ".join(str_surrounding)}")
    loss += board.size - len(occupied_regions) # 2 queens 1 region    
    
    return loss
            

def update_regions(board: Board, queen_list: list[Queen]):
    for queen in queen_list:
        r = queen.row
        c = queen.col
        queen.region = board.cells[r][c].region

def solve(board: Board, renderer: BoardRenderer = None):
    if not board:
        raise ValueError("AYO WHERES THE BOARD")
    
    queens_list: list[Queen] = queen_setter(board)
    
    solved = False
    while not solved:
        
        update_regions(board, queens_list)

        loss = calculate_loss(board, queens_list)
        print(f"Loss: {loss}")
        if loss == 0:
            solved = True
            break
        
        if renderer:
            renderer.update(board, queens_list)
        
        # choose random queen from first set of queens in the same region.
        for q1 in range(len(queens_list)):
            queen1: Queen = queens_list[q1]
            for q2 in range(q1+1, len(queens_list)):
                queen2: Queen = queens_list[q2]
                if queen1.region == queen2.region:
                    # choose randomly
                    chosen_q: Queen = random.choice([queen1, queen2])
                    break

        other_q: Queen = random.choice([queen for queen in queens_list if queen != chosen_q]) 

        chosen_q_col = chosen_q.col
        chosen_q.col = other_q.col
        other_q.col = chosen_q_col
        
        # regions get updated in next iteration
        # randomly find a queen in a duped region and swap her column with another random queen
    return queens_list  