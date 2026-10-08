from base import Board
from puzzleGenerator import queen_setter, region_creator, surrounding_cells
import random

from renderer import BoardRenderer
BOARD_SIZE = 8 # this means there are 8 colours too

'''TO DO: CLEAN UP. 
 - Loss must also take diagonals into account
 - Swaps must be made even if all regions are set (now that diags can occur)'''

        
def calculate_loss(board: Board, queen_list: list):
    '''calculate the current loss'''
    occupied_regions = set()
    for queen in queen_list:
        occupied_regions.add(queen["region"])
        
    loss = board.size - len(occupied_regions) # 2 queens 1 region
    
    # loop through all queens and use functionality to test each diagonal
    for queen in queen_list:
        for cell in surrounding_cells(board, queen["row"], queen["col"]):
            if cell.q:
                loss += 1
            
    
    # int_set = {i for i in range(board.size)}
    # missed_regions = int_set.difference(occupied_regions)
    # need to count for adjacent queens. The init solution will guarantee one queen per row and column.
    return loss
            
        
# How to make this work:
'''
RL method -> not ideal since the rules of the game would have to be learnt
search:
1. uninformed -> wayyy too long. But could start with smallest region
2. informed -> definitely the way to go.
Graph of states with edges: start with a random configuration (n queens placed) <-

Or start with an empty board a choose one placement in the smallest region. - greedy approach

third - use remembered patterns to force queen placement >:)'''

'''Graph of states with edges: start with a random configuration (n queens placed):
RULES: initial board set up has 1 queen in every row and column (in a diagonal say)
1. Loss function = # of collisions (queens in same region) - there can never be queens in the same row or diagonal
2. allowed moves/edges = swap any 2 queen's column. Row's stay 'untouched'. Regions can define the range of a swap
    - e.g., if there exists a region that lives ONLY in row 'n', then the queen cann
Algorithm:
queen init (diag)
calculate loss
make random swap <- insert better method
calculate loss

What I want for quick look up -? cell co-ords, queen co-ords
'''

def update_regions(board, queen_list):
    for queen in queen_list:
        r = queen["row"]
        c = queen["col"]
        queen["region"] = board.cells[r][c].region

def solve(board: Board):
    if not board:
        raise ValueError("AYO WHERES THE BOARD")
    
    queens_list = queen_setter(board) # initial queen setting
    print(queens_list)
    solved = False
    while not solved:
        
        # print(board.cells[0][0])
        update_regions(board, queens_list)
        # Calculate loss - if 0 solved :)

        loss = calculate_loss(board, queens_list)
        if loss == 0:
            solved = True
            break
        
        # choose random queen from first set of queens in the same region.
        for q1 in range(len(queens_list)):
            queen1 = queens_list[q1]
            for cell in surrounding_cells(board, queen1["row"], queen1["col"]): # loops through max 4 cells min 1 cell
                if cell.q:
                    chosen_q = random.choice([queen1, cell.q])
                    break
                
            for q2 in range(q1+1, len(queens_list)):
                queen2 = queens_list[q2]
                if queen1["region"] == queen2["region"]:
                    # choose randomly
                    chosen_q = random.choice([queen1, queen2])
                    break
                
                    
        # choose a random different queen
        
        rand_idx = random.choice([i for i in range(len(queens_list)) if i != chosen_q])
        q2 = queens_list[rand_idx]

        # swap cols between the two queens
        q1_col = chosen_q["col"]
        
        board.cells[q1_col][chosen_q["row"]].q = None
        board.cells[q2["col"]][chosen_q["row"]].q = q1
        board.cells[q1_col][q2["row"]].q = q2
        board.cells[q2["col"]][q2["row"]].q = None
        
        chosen_q["col"] = q2["col"]
        q2["col"] = q1_col
        
        # regions get updated in next iteration
        # randomly find a queen in a duped region and swap her column with another random queen
    return queens_list  