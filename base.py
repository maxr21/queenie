class Cell: # Record
    '''Cells have rows, columns and regions'''
    def __init__(self, region: int, row: int, col: int):
        self.region = region
        self.row = row
        self.col = col
        
    def __str__(self):
        return f"region: {self.region}, row: {self.row}, col: {self.col}"
    
    def __repr__(self):
        return self.__str__()

class Board:
    '''Board class represent a queens board.
    The board can have queens on it and is made up of cells'''
    def __init__(self, size: int):
        self.size = size
        self.cells = []
        self.queens = [] # list of dict to queen position+region
        self._build_board()
        
    def _build_board(self):
        for row in range(self.size):
            self.cells.append([])
            for col in range(self.size):
                self.cells[row].append(Cell(-1, row, col))
        
    def init_queens(self):
        '''Initialises the start state of the board by placing all queens along a diagonal'''
        if not len(self.queens) == 0: # there are already queens about!
            raise
        
        for i in range(self.size):
            self.queens.append({"row": i, "col": i, "region": i})
    
    def make_swap(self, q1: int, q2: int):
        '''swap two queen's columns'''
        if q1 == q2: # same queen
            raise
        q1_col = self.queens[q1]["col"]
        self.queens[q1]["col"] = self.queens[q2]["col"]
        self.queens[q2]["col"] = q1_col